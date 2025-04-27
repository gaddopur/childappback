from django.urls import path
from django.conf.urls.static import static
from childappback import settings
from .views import QuerySolver, SummarizePdfView

urlpatterns = [
    path('solvequery/', QuerySolver.as_view({'post': 'solveQuery'}), name='solve_query'),
    path('pdf_summerizer/', SummarizePdfView.as_view(), name='summarize_pdf'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)