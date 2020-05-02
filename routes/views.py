from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from routes.forms import RouteForm, RouteModelForm
from routes.models import Route
from trains.models import Train
import time as tm


def dfs_paths(graph, start, goal):
    """
    Функція поиска всіх можливих маршрутів
    із одного міста в інший. Варіант відвідування
    одного и того же міста більше одного раза,
    не розглядається.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(_qs):
    """
    Функция по творенню графа из БД по розкладу
    руху поїздів для работи функції dfs_paths 
    """
    qs = _qs.values()
    graph = {}
    for q in qs:
        graph.setdefault(q['from_city_id'], set())
        graph[q['from_city_id']].add(q['to_city_id'])
    return graph


def home(request):
    """Функція головної сторінки"""
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    """Пошук маршруту"""
    if request.method == "POST":
        start = tm.time()
        form = RouteForm(request.POST or None)
        if form.is_valid():
            qs = Train.objects.all().order_by('travel_time')
            data = form.cleaned_data
            from_city = data['from_city']
            to_city = data['to_city']
            cities = data['cities']
            travelling_time = data['travelling_time']
            graph = get_graph(_qs=qs)
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
            if len(all_ways) == 0:
                # нема жодного маршруто для заданого пошуку
                messages.error(request,
                               'Маршруту, задовільняющого умови не існує.')
                return render(request, 'routes/home.html', {'form': form})
            if cities:
                # якщо є міста через які потрібно проїхати
                across_cities = [city.id for city in cities]
                right_ways = []
                for way in all_ways:
                    # тоді відбираєм ті маршрути, які проходять через них
                    if all(point in way for point in across_cities):
                        right_ways.append(way)
                if not right_ways:
                    # коли список маршрутів пустий
                    messages.error(request, 'Маршрут через ці міста неможливий')
                    return render(request, 'routes/home.html', {'form': form})
            else:
                right_ways = all_ways
            trains = []
            all_trains = {}
            for q in qs:
                all_trains.setdefault((q.from_city_id, q.to_city_id), [])
                all_trains[(q.from_city_id, q.to_city_id)].append(q)
            for route in right_ways:
                # для міст по дорозі маршруту, вибираем необхідні потяги
                tmp = {}
                tmp['trains'] = []
                total_time = 0
                for index in range(len(route) - 1):
                    qs = all_trains[(route[index], route[index + 1])]
                    qs = qs[0]
                    total_time += qs.travel_time
                    tmp['trains'].append(qs)
                tmp['total_time'] = total_time
                if total_time <= travelling_time:
                    # якщо загальний час в дорозі менше заданого,
                    # то добавляем маршрут в загальний список
                    trains.append(tmp)
            if not trains:
                # якщо список пустий, то нема ніяких маршрутів,
                # які б задовільнили задані умови
                messages.error(request, 'Час в дорозі, більше заданного.')
                return render(request, 'routes/home.html', {'form': form})
            routes = []
            cities = {'from_city': from_city.name, 'to_city': to_city.name}
            for tr in trains:
                # формуюю список всіх маршрутов
                routes.append({'route': tr['trains'],
                               'total_time': tr['total_time'],
                               'from_city': from_city.name,
                               'to_city': to_city.name})
            sorted_routes = []
            if len(routes) == 1:
                sorted_routes = routes
            else:
                # якщо маршрутів більше одного, то сортую їх по часу
                times = list(set(x['total_time'] for x in routes))
                times = sorted(times)
                for time in times:
                    for route in routes:
                        if time == route['total_time']:
                            sorted_routes.append(route)
            context = {}
            form = RouteForm()
            context['form'] = form
            context['routes'] = sorted_routes
            context['cities'] = cities
            context['time'] = tm.time() - start
            return render(request, 'routes/home.html', context)
    else:
        messages.error(request, 'Створіть маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    """Збереження маршруту"""
    if request.method == 'POST':
        form = RouteModelForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            travel_times = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            trains = data['trains'].split(' ')
            trains_lst = [int(x) for x in trains if x.isdigit()]
            qs = Train.objects.filter(id__in=trains_lst)
            route = Route(name=name, from_city=from_city,
                          to_city=to_city, travel_times=travel_times)
            route.save()  # збереження нового маршруту
            for tr in qs:  # збереження в маршрут, потягів из списка
                route.trains.add(tr.id)
            messages.success(request, 'Маршрут було вдало збережено.')
            return redirect('/')
        messages.error(request, 'Неправильно заповнена форма')
        return redirect('/')
    else:
        data = request.GET
        if data:
            travel_times = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            trains = data['trains'].split(' ')
            trains_lst = [int(x) for x in trains if x.isdigit()]
            qs = Train.objects.filter(id__in=trains_lst)
            train_list = ' '.join(str(i) for i in trains_lst)
            form = RouteModelForm(
                initial={'from_city': from_city, 'to_city': to_city,
                         'travel_times': travel_times, 'trains': train_list})
            context = {}
            route_desc = []
            for tr in qs:
                dsc = '''Потяг №{} направляющийся з {} в {}.
            Час в дорозі {}.'''.format(tr.name, tr.from_city, tr.to_city,
                                       tr.travel_time)
                route_desc.append(dsc)
            context = {'form': form, 'descr': route_desc,
                       'from_city': from_city,
                       'to_city': to_city, 'travel_times': travel_times}
            return render(request, 'routes/create.html', context)
        else:
             # захист від звернень по адресі баз данних
            messages.error(request, 'Неможливо зберегти неіснуючий маршрут')
            return redirect('/')


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    context_object_name = 'object'
    template_name = 'routes/detail.html'


class RouteListView(ListView):
    queryset = Route.objects.all()
    context_object_name = 'objects_list'
    template_name = 'routes/list.html'


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('home')
    login_url = 'accounts/login/'

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут видалено!')
        return self.post(request, *args, **kwargs)
