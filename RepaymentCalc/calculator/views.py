from django.shortcuts import render
from decimal import Decimal
def index(request):
    #если пришел метод ПОСТ вызываем calculate_payments
    #иначе как есть работаем
    if request.method == 'POST' or (request.method == 'GET' and request.GET.get('calculate') == 1):
        #return calculate_payments(request)
        calc_result = calculate_payments_simple(request)
        return render(request, 'calculator/result.html', calc_result)
    else:
        return render(request, 'calculator/index.html')

def calculate_payments_simple(request):
    data = request.POST
    print(data)
    names = data.getlist('name', [])
    amounts = data.getlist('amount', [])
    interest_rates = data.getlist('interest_rate', [])
    terms = data.getlist('term', [])
    credits_data = []
    for i in range(len(names)):
        credits_data.append({
            'name': names[i],
            'amount': amounts[i],
            'interest_rate': interest_rates[i],
            'term': terms[i],
        })
    method = data.get('method', 'avalanche')
    monthly_payment = Decimal(data.get('monthlyPayment', 0))

    credits = []

    for credit_data in credits_data:
        credit = {
            'name': credit_data['name'],
            'amount': Decimal(credit_data['amount']),
            'interest_rate': Decimal(credit_data['interest_rate']),
            'term': int(credit_data['term']),
            'remaining': Decimal(credit_data['amount'])
        }
        credits.append(credit)

    if method == 'avalanche':
        result = calculate_avalanche(credits, monthly_payment)
    else:
        result = calculate_snowball(credits, monthly_payment)
    return result



def calculate_avalanche(credits, monthly_payment): #выполнение расчетов методом лавина
    """Метод лавины - сначала погашаем кредиты с наибольшей процентной ставкой"""
    months = 0
    total_interest = Decimal('0')
    schedule = []
    months_break = False
    # сортируем кредиты по убыванию процентной ставки
    sorted_credits = sorted(credits, key=lambda x: x['interest_rate'], reverse=True)
    # прерываем если слишком много месяцев
    if months > 360:  # максимум 30 лет
        months = 360
        months_break = True

    while any(credit['remaining'] > 0 for credit in sorted_credits):
        months += 1
        month_data = {'month': months, 'payments': [], 'total_paid': Decimal('0')}
        # вычисляем минимальные платежи
        total_min_payment = Decimal('0')
        for credit in sorted_credits:
            if credit['remaining'] > 0:
                interest = credit['remaining'] * (credit['interest_rate'] / 100 / 12)
                min_payment = interest + (credit['remaining'] / credit['term'])
                total_min_payment += min_payment

        # распределяем дополнительный платеж
        available_extra = monthly_payment - total_min_payment
        #print(total_min_payment, monthly_payment, available_extra)

        for credit in sorted_credits:
            if credit['remaining'] > 0:
                interest = credit['remaining'] * (credit['interest_rate'] / 100 / 12)
                min_payment = interest + (credit['remaining'] / credit['term'])

                # для кредита с наибольшей ставкой добавляем дополнительный платеж
                if credit == sorted_credits[0] and available_extra > 0:
                    payment = min_payment + available_extra
                else:
                    payment = min_payment

                payment = min(payment, credit['remaining'] + interest)
                principal = payment - interest

                month_data['payments'].append({
                    'name': credit['name'],
                    'interest': float(interest),
                    'principal': float(principal),
                    'total_payment': float(payment),
                    'remaining': float(credit['remaining'] - principal)
                })

                credit['remaining'] -= principal
                total_interest += interest
                month_data['total_paid'] += payment

        schedule.append(month_data)


    print({
        'method': 'avalanche',
        'total_months': months,
        'total_interest': float(total_interest),
        'schedule': schedule
    })
    return {
        'method': 'avalanche',
        'total_months': months,
        'months_break': months_break,
        'total_interest': float(total_interest),
        'schedule': schedule
    }


def calculate_snowball(credits, monthly_payment):
    """Метод снежного кома - сначала погашаем кредиты с наименьшей суммой"""
    months = 0
    total_interest = Decimal('0')
    schedule = []

    # Сортируем кредиты по возрастанию оставшейся суммы
    sorted_credits = sorted(credits, key=lambda x: x['remaining'])

    while any(credit['remaining'] > 0 for credit in sorted_credits):
        months += 1
        month_data = {'month': months, 'payments': [], 'total_paid': Decimal('0')}

        # Вычисляем минимальные платежи
        total_min_payment = Decimal('0')
        for credit in sorted_credits:
            if credit['remaining'] > 0:
                interest = credit['remaining'] * (credit['interest_rate'] / 100 / 12)
                min_payment = interest + (credit['remaining'] / credit['term'])
                total_min_payment += min_payment

        # Распределяем дополнительный платеж на самый маленький кредит
        available_extra = monthly_payment - total_min_payment

        for credit in sorted_credits:
            if credit['remaining'] > 0:
                interest = credit['remaining'] * (credit['interest_rate'] / 100 / 12)
                min_payment = interest + (credit['remaining'] / credit['term'])

                # Для самого маленького кредита добавляем дополнительный платеж
                if credit == sorted_credits[0] and available_extra > 0:
                    payment = min_payment + available_extra
                    available_extra = Decimal('0')  # Используем только для первого кредита
                else:
                    payment = min_payment

                payment = min(payment, credit['remaining'] + interest)
                principal = payment - interest

                month_data['payments'].append({
                    'name': credit['name'],
                    'interest': float(interest),
                    'principal': float(principal),
                    'total_payment': float(payment),
                    'remaining': float(credit['remaining'] - principal)
                })

                credit['remaining'] -= principal
                total_interest += interest
                month_data['total_paid'] += payment

        schedule.append(month_data)

        # Прерываем если слишком много месяцев
        if months > 600:
            break

        # Пересортируем кредиты по оставшейся сумме
        sorted_credits = sorted([c for c in sorted_credits if c['remaining'] > 0],
                                key=lambda x: x['remaining'])

    return {
        'method': 'snowball',
        'total_months': months,
        'total_interest': float(total_interest),
        'schedule': schedule
    }