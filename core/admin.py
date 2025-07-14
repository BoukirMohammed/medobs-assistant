from django.contrib import admin
from .models import Service, Competence, TemplateObservation, Observation, FichierMedia, Evaluation, EvaluationCompetence

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'date_creation')
    search_fields = ('nom', 'description')
    ordering = ('nom',)

@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'date_creation')
    search_fields = ('nom', 'description')
    ordering = ('nom',)

@admin.register(TemplateObservation)
class TemplateObservationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'service', 'cree_par', 'actif', 'date_creation')
    list_filter = ('service', 'actif', 'date_creation')
    search_fields = ('nom', 'service__nom')
    filter_horizontal = ('competences_evaluees',)

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'etudiant', 'template', 'statut', 'date_creation', 'date_soumission')
    list_filter = ('statut', 'template__service', 'date_creation')
    search_fields = ('etudiant__username', 'etudiant__first_name', 'etudiant__last_name')
    readonly_fields = ('date_creation', 'date_modification')

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('observation', 'professeur', 'date_evaluation')
    list_filter = ('date_evaluation', 'professeur')
    search_fields = ('observation__etudiant__username', 'professeur__username')