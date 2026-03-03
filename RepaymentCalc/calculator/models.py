from django.db import models

class Credit(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название кредита")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Оставшаяся сумма кредита")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процентная ставка (%)")
    term = models.IntegerField(verbose_name="Оставшийся срок (месяцев)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кредит"
        verbose_name_plural = "Кредиты"