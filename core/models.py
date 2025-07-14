from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Utilisateur


# === MODÈLES DE STRUCTURE ET ORGANISATION ===

class Service(models.Model):
    """Représente un service médical (ex: Cardiologie, Neurologie)."""
    nom = models.CharField(max_length=150, unique=True, verbose_name="Nom du service")
    description = models.TextField(blank=True, verbose_name="Description")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Médical"
        verbose_name_plural = "Services Médicaux"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Competence(models.Model):
    """Représente une compétence clinique évaluable."""
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la compétence")
    description = models.TextField(blank=True, verbose_name="Critères d'évaluation")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class TemplateObservation(models.Model):
    """Template d'observation créé par un professeur."""
    nom = models.CharField(max_length=255, verbose_name="Nom du template")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="templates")
    cree_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'PROFESSEUR'},
        verbose_name="Créateur"
    )
    structure = models.JSONField(
        verbose_name="Structure du formulaire",
        help_text="Structure JSON décrivant les compétences et les questions du template."
    )
    competences_evaluees = models.ManyToManyField(Competence, blank=True, verbose_name="Compétences couvertes")
    date_creation = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True, verbose_name="Template actif")

    class Meta:
        verbose_name = "Template d'Observation"
        verbose_name_plural = "Templates d'Observation"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.nom} ({self.service.nom})"


# === MODÈLES LIÉS AU TRAVAIL DE L'ÉTUDIANT ===

class Observation(models.Model):
    """Observation concrète créée et remplie par un étudiant."""

    class Statut(models.TextChoices):
        BROUILLON = 'BROUILLON', 'Brouillon'
        EN_ATTENTE = 'EN_ATTENTE', 'En attente de relecture'
        A_CORRIGER = 'A_CORRIGER', 'À corriger'
        VALIDEE = 'VALIDEE', 'Validée'

    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="observations",
        limit_choices_to={'role': 'ETUDIANT'}
    )
    template = models.ForeignKey(
        TemplateObservation,
        on_delete=models.PROTECT,
        related_name="observations"
    )
    statut = models.CharField(max_length=15, choices=Statut.choices, default=Statut.BROUILLON)
    donnees = models.JSONField(blank=True, null=True, verbose_name="Données saisies")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_soumission = models.DateTimeField(null=True, blank=True, verbose_name="Date de soumission")

    class Meta:
        verbose_name = "Observation"
        verbose_name_plural = "Observations"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Observation #{self.id} de {self.etudiant.username}"


class FichierMedia(models.Model):
    """Fichier uploadé et lié à une observation."""
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE, related_name="fichiers")
    fichier = models.FileField(upload_to='fichiers_observations/%Y/%m/', verbose_name="Fichier")
    legende = models.CharField(max_length=255, blank=True, verbose_name="Légende")
    date_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fichier Média"
        verbose_name_plural = "Fichiers Média"

    def __str__(self):
        return f"Fichier {self.id} pour l'observation #{self.observation.id}"


# === MODÈLES D'ÉVALUATION ===

class Evaluation(models.Model):
    """Évaluation d'une observation par un professeur."""
    observation = models.OneToOneField(
        Observation,
        on_delete=models.CASCADE,
        related_name="evaluation"
    )
    professeur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name="evaluations_faites",
        limit_choices_to={'role': 'PROFESSEUR'}
    )
    commentaires_generaux = models.TextField(blank=True, verbose_name="Commentaires Généraux")
    date_evaluation = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Évaluation"
        verbose_name_plural = "Évaluations"

    def __str__(self):
        return f"Évaluation pour l'Observation #{self.observation.id}"


class EvaluationCompetence(models.Model):
    """Note d'une compétence spécifique pour une évaluation."""
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="notes_competences")
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    note = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note"
    )
    commentaire_specifique = models.TextField(blank=True, verbose_name="Commentaire spécifique")

    class Meta:
        unique_together = ('evaluation', 'competence')
        verbose_name = "Note par Compétence"
        verbose_name_plural = "Notes par Compétence"

    def __str__(self):
        return f"Note pour {self.competence.nom}: {self.note}/5"