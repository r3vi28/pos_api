from django.core.paginator import Paginator
from .response import Result


def Paginar(queryset, serializer_class, request):
    """
    Pagina cualquier queryset de forma reutilizable.

    queryset: los datos ya filtrados/ordenados (ej: Producto.objects.all())
    serializer_class: la clase del serializer a usar (ej: ProductoSerializer)
    request: el objeto request para leer 'page' y 'pagesize' de la URL
    """
    page = request.GET.get('page', 1)
    pagesize = request.GET.get('pagesize', 10)

    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        pagesize = int(pagesize)
    except ValueError:
        pagesize = 10

    paginator = Paginator(queryset, pagesize)
    total_pages = paginator.num_pages

    if page > total_pages or page < 1:
        return Result.ErrorResponsePaginator(
            f"No existe la página {page}. Páginas disponibles: 1 a {total_pages}.",
            total_pages,
            page
        )

    page_obj = paginator.page(page)

    button_previous = page_obj.has_previous()
    button_next = page_obj.has_next()

    serializer = serializer_class(page_obj, many=True)

    return Result.ResponsePaginator('', serializer.data, total_pages, page, button_previous, button_next)