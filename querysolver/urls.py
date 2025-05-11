from django.urls import path
from django.conf.urls.static import static
from childappback import settings
from .views import QuerySolver, SummarizePdfView, MathSolver

urlpatterns = [
    path('solvequery/', QuerySolver.as_view({'post': 'solveQuery'}), name='solve_query'),
    path('pdf_summerizer/', SummarizePdfView.as_view(), name='summarize_pdf'),
    path('math_solver/', MathSolver.as_view(), name='math_solver'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)