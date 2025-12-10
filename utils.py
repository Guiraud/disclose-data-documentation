"""
Utilitaires pour le projet Disclose Data

Ce module contient des fonctions utilitaires réutilisables :
- Retry logic pour les appels API
- Gestion d'erreurs robuste
- Logging configuré
- Validation des paramètres
"""

import time
import logging
from typing import Any, Callable, Optional, TypeVar, cast
from functools import wraps
from datetime import datetime

# Type générique pour les fonctions
T = TypeVar('T')

# Configuration du logging
logger = logging.getLogger("disclose-data")


class DiscloseDataError(Exception):
    """Exception de base pour les erreurs Disclose Data"""
    pass


class APIError(DiscloseDataError):
    """Erreur lors d'un appel API"""
    pass


class ValidationError(DiscloseDataError):
    """Erreur de validation des paramètres"""
    pass


class RateLimitError(DiscloseDataError):
    """Erreur de rate limit"""
    pass


def retry_on_error(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """
    Décorateur pour réessayer une fonction en cas d'erreur avec backoff exponentiel.

    Args:
        max_attempts: Nombre maximum de tentatives (défaut: 3)
        initial_delay: Délai initial en secondes (défaut: 1.0)
        backoff_factor: Facteur multiplicateur pour le délai (défaut: 2.0)
        exceptions: Tuple des exceptions à intercepter (défaut: (Exception,))

    Example:
        @retry_on_error(max_attempts=3, initial_delay=2.0)
        def ma_fonction_api():
            return client.get_data()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delay = initial_delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        logger.error(
                            f"Échec après {max_attempts} tentatives: {func.__name__}"
                        )
                        raise

                    logger.warning(
                        f"Tentative {attempt}/{max_attempts} échouée pour {func.__name__}: {e}"
                    )
                    logger.info(f"Nouvelle tentative dans {delay:.1f}s...")
                    time.sleep(delay)
                    delay *= backoff_factor

            # Ne devrait jamais arriver ici, mais pour satisfaire le type checker
            if last_exception:
                raise last_exception
            raise RuntimeError("Erreur inattendue dans retry_on_error")

        return wrapper
    return decorator


def validate_date_format(date_str: str) -> bool:
    """
    Valider le format d'une date (YYYY-MM-DD).

    Args:
        date_str: Chaîne de date à valider

    Returns:
        True si le format est valide, False sinon

    Example:
        >>> validate_date_format("2024-01-15")
        True
        >>> validate_date_format("2024/01/15")
        False
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_department_code(code: str) -> bool:
    """
    Valider un code département français.

    Args:
        code: Code département à valider

    Returns:
        True si le code est valide, False sinon

    Example:
        >>> validate_department_code("75")
        True
        >>> validate_department_code("2A")
        True
        >>> validate_department_code("999")
        False
    """
    # Codes valides : 01-19, 2A, 2B, 21-95, 971-976
    if not code:
        return False

    # Corse
    if code in ["2A", "2B"]:
        return True

    # Numérique
    try:
        num = int(code)
        # Métropole (01-95) ou DOM-TOM (971-976)
        return (1 <= num <= 95) or (971 <= num <= 976)
    except ValueError:
        return False


def validate_category(category: str) -> bool:
    """
    Valider une catégorie de document.

    Args:
        category: Catégorie à valider

    Returns:
        True si la catégorie est valide, False sinon

    Example:
        >>> validate_category("Avis")
        True
        >>> validate_category("InvalidCategory")
        False
    """
    valid_categories = ["Avis", "Cadrage", "Cas par Cas"]
    return category in valid_categories


def safe_get_attribute(obj: Any, attr: str, default: Any = None) -> Any:
    """
    Récupérer un attribut d'un objet de manière sécurisée.

    Args:
        obj: Objet à interroger
        attr: Nom de l'attribut
        default: Valeur par défaut si l'attribut n'existe pas

    Returns:
        Valeur de l'attribut ou valeur par défaut

    Example:
        >>> safe_get_attribute(doc, 'title', 'Sans titre')
        'Mon document'
    """
    try:
        return getattr(obj, attr, default)
    except AttributeError:
        return default


def safe_dict_get(data: Optional[dict], key: str, default: Any = None) -> Any:
    """
    Récupérer une valeur dans un dictionnaire de manière sécurisée.

    Args:
        data: Dictionnaire (peut être None)
        key: Clé à récupérer
        default: Valeur par défaut

    Returns:
        Valeur ou valeur par défaut

    Example:
        >>> safe_dict_get({'name': 'Test'}, 'name', 'Unknown')
        'Test'
        >>> safe_dict_get(None, 'name', 'Unknown')
        'Unknown'
    """
    if data is None:
        return default
    return data.get(key, default)


def format_number(num: int) -> str:
    """
    Formater un nombre avec des séparateurs de milliers.

    Args:
        num: Nombre à formater

    Returns:
        Chaîne formatée

    Example:
        >>> format_number(1234567)
        '1 234 567'
    """
    return f"{num:,}".replace(",", " ")


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Tronquer un texte à une longueur maximale.

    Args:
        text: Texte à tronquer
        max_length: Longueur maximale
        suffix: Suffixe à ajouter si tronqué

    Returns:
        Texte tronqué

    Example:
        >>> truncate_text("Un texte très long...", 10)
        'Un texte...'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


class ProgressTracker:
    """
    Tracker de progression simple pour les opérations longues.

    Example:
        tracker = ProgressTracker(total=100)
        for i in range(100):
            tracker.update()
        tracker.finish()
    """

    def __init__(self, total: int, description: str = "Progression"):
        """
        Initialiser le tracker.

        Args:
            total: Nombre total d'items
            description: Description de la progression
        """
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()

    def update(self, increment: int = 1) -> None:
        """
        Mettre à jour la progression.

        Args:
            increment: Nombre d'items traités
        """
        self.current += increment
        percentage = (self.current / self.total) * 100 if self.total > 0 else 0

        if self.current % max(1, self.total // 10) == 0 or self.current == self.total:
            elapsed = time.time() - self.start_time
            rate = self.current / elapsed if elapsed > 0 else 0
            logger.info(
                f"{self.description}: {self.current}/{self.total} "
                f"({percentage:.1f}%) - {rate:.1f} items/s"
            )

    def finish(self) -> None:
        """Finaliser la progression."""
        elapsed = time.time() - self.start_time
        logger.info(
            f"{self.description} terminé: {self.current}/{self.total} "
            f"en {elapsed:.1f}s"
        )


def configure_logging(level: str = "INFO", format_string: Optional[str] = None) -> None:
    """
    Configurer le logging pour l'application.

    Args:
        level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Format personnalisé pour les logs

    Example:
        configure_logging(level="DEBUG")
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        datefmt="%Y-%m-%d %H:%M:%S"
    )


# Exemples d'utilisation
if __name__ == "__main__":
    # Configurer le logging
    configure_logging(level="INFO")

    # Test de retry
    @retry_on_error(max_attempts=3, initial_delay=0.5)
    def fonction_test():
        logger.info("Appel de fonction_test")
        return "Success"

    result = fonction_test()
    print(f"Résultat: {result}")

    # Test de validation
    print(f"Date valide: {validate_date_format('2024-01-15')}")
    print(f"Département valide: {validate_department_code('75')}")
    print(f"Catégorie valide: {validate_category('Avis')}")

    # Test de formatage
    print(f"Nombre formaté: {format_number(1234567)}")
    print(f"Texte tronqué: {truncate_text('Un texte très long qui doit être tronqué', 20)}")
