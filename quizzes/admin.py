from django.contrib import admin

# Register your models here.
from .models import Quiz, Question, Choice, Result
class Choiceinline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [Choiceinline]

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result)