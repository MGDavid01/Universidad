from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Category

CATEGORIES = [
    ("Redes / Wi‑Fi", "redes", "Conectividad, routers, APs y cableado."),
    ("Hardware / PCs", "hardware", "Equipos de cómputo, fuentes, motherboards y periféricos."),
    ("Ciberseguridad básica", "seguridad", "Antivirus, backups y hardening ligero."),
    ("Software / sistemas", "software", "Instalación, configuración y soporte de aplicaciones."),
]


class Command(BaseCommand):
    help = "Crea categorías técnicas iniciales si no existen."

    def handle(self, *args, **options):
        created = 0
        for name, slug, description in CATEGORIES:
            _, was_created = Category.objects.get_or_create(
                slug=slug or slugify(name),
                defaults={"name": name, "description": description},
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Categorías listas. Nuevas: {created}"))
