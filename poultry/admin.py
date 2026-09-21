from django.contrib import admin
from .models import (
    Farm,
    Batch,
    DailyRecord,
    EggProduction,
    Expense,
    Sale,
)


admin.site.register(Farm)
admin.site.register(Batch)
admin.site.register(DailyRecord)
admin.site.register(EggProduction)
admin.site.register(Expense)
admin.site.register(Sale)