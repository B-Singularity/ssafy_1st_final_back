import logging
from dependency_injector import containers, providers
from .application.services import MovieAppService
from .infrastructure.persistence.repositories import DjangoMovieRepository, DjangoMovieSearchRepository

logger = logging.getLogger(__name__)

class MovieContainer(containers.DeclarativeContainer):
    logger.info("Initializing MovieContainer")

    movie_repository = providers.Factory(DjangoMovieRepository)
    movie_search_repository = providers.Factory(DjangoMovieSearchRepository)

    movie_app_service = providers.Factory(
        MovieAppService,
        movie_repository=movie_repository,
        movie_search_repository=movie_search_repository,
    )