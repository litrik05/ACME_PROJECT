from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


def birthday(request, pk=None):
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
        # Создаём экземпляр класса формы.
        # (если получен запрос к странице создания записи):
        # Преобразуем дату в формат ГГГГ-ММ-ДД для HTML5 виджета
        initial_data = {'birthday': instance.birthday.strftime('%Y-%m-%d')}
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
        initial_data = None

    # Передаём в форму либо данные из запроса, либо None.
    # В случае редактирования прикрепляем объект модели.
    form = BirthdayForm(request.POST or None,
                        files=request.FILES or None,
                        instance=instance, initial=initial_data)
    context = {'form': form}
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    # Добавляем его в словарь контекста под ключом form:
    return render(request, 'birthday/birthday.html', context=context)


def birthday_list(request):
    # Получаем все объекты модели Birthday из БД.
    # Получаем список всех объектов с сортировкой по id.
    birthdays = Birthday.objects.order_by('id')

    # Создаём объект пагинатора с количеством 10 записей на страницу.
    paginator = Paginator(birthdays, 3)

    # Получаем из запроса значение параметра page.
    page_number = request.GET.get('page')
    # Если параметра page нет в запросе или его значение не приводится к числу,
    # вернётся первая страница.
    page_obj = paginator.get_page(page_number)

    # Передаём их в контекст шаблона.
    # context = {'birthdays': birthdays}
    context = {'page_obj': page_obj}
    return render(request, 'birthday/birthday_list.html', context)


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)
