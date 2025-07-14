from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    """
    Modèle utilisateur personnalisé qui étend le modèle de base de Django.
    Il est central pour l'ensemble de l'application car il gère les rôles
    et les permissions implicites.
    """

    class Role(models.TextChoices):
        ETUDIANT = 'ETUDIANT', 'Étudiant'
        PROFESSEUR = 'PROFESSEUR', 'Professeur'

    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        verbose_name="Rôle de l'utilisateur"
    )

    service_rattachement = models.ForeignKey(
        'core.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Service de rattachement (si professeur)"
    )

    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"