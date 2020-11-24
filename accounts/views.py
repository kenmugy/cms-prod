from datetime import date
from django.shortcuts import render, get_object_or_404,get_list_or_404, redirect
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from .models import *
from .forms import *
from .decorators import authenticated_user, allowed_user, admin_only

# Create your views here.
@authenticated_user
def loginView(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			success(request,'Logged in')
			login(request, user)
			return redirect('dashboard')

	return render(request, 'accounts/login.html')

def logoutView(request):
	logout(request)
	return redirect('login')
	 
@login_required
@admin_only
def dashboard(request):
	# orders = Order.objects.all().order_by('-date_created')
	orders = Order.objects.filter(date_created__date=date.today()).order_by('-date_created')
	p_orders = orders.filter(status="Pending")
	d_orders = orders.filter(status="Delivered")
	customers = Customer.objects.filter()
	context = {
		'orders': orders,
		'f_orders': orders[:5],
		'customers': customers,
		'total_orders': orders.count(),
		'p_orders': p_orders.count(),
		'd_orders':d_orders.count(),
	}
	return render(request, 'accounts/dashboard.html', context)

@login_required
@allowed_user(allowed_roles=['store'])
def items(request):
	form = ItemCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('items')
	queryset = Item.objects.all().order_by('-date_created')
	context = {
		'form': form,
		'items': queryset
	}
	return render(request, 'accounts/items.html', context)

@login_required
def orders(request):
	return render(request, 'accounts/orders.html', {})

@login_required
@allowed_user(allowed_roles=['store'])
@admin_only
def customers(request, pk):
	customer = get_object_or_404(Customer, id=pk)
	form = OrderSearchForm(request.POST or None)
	# total_orders = customer.order_set.all().order_by('-date_created')
	orders = customer.order_set.all().filter(date_created__date=date.today()).order_by('-date_created')
	p_orders = orders.filter(status="Pending").count()
	orders_count = orders.count()
	context = {
		'customer': customer, 
		'p_orders': p_orders, 
		'orders': orders, 
		'orders_count':orders_count, 
		'form': form
		}
	
	if request.method == 'POST':
		
		orders = customer.order_set.filter(
			name__icontains = form['name'].value(),
			status__icontains = form['status'].value())
		context = {
			'customer': customer,  
			'p_orders': p_orders, 
			'orders': orders, 
			'orders_count':orders_count, 
			'form': form
			}

	return render(request, 'accounts/customers.html', context )

@login_required 
def create_order(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields = ("name", "quantity"), extra=10)

	# if not request.user.customer:
	#     OrderFormSet = inlineformset_factory(Customer, Order, fields = ( "status"), extra=3)
	customer = get_object_or_404(Customer, id=pk)
	# form = OrderForm(request.POST or None, initial = {"customer":customer})
	formset = OrderFormSet(request.POST or None,queryset = Order.objects.none(), instance=customer)
	if formset.is_valid():
		formset.save()
		# return redirect(f'/customers/{customer.id}')
		if request.user.customer:
			return redirect('user')
		else:
			return redirect('dashboard')
	return render(request, 'accounts/order_form.html', {"form1": formset})

@login_required
def update_order(request, pk):
	orderquery = get_object_or_404(Order, id=pk)
	# form = OrderForm(request.POST or None, instance=orderquery,)
	form1 = OrderForm(request.POST or None, instance=orderquery)
	form2 = StoreOrderForm(request.POST or None, instance=orderquery)
	context = {
		'form1': form1,
		'form2': form2,
	}
	if form1.is_valid():
		form1.save()
		return redirect('user')
	elif form2.is_valid():
		form2.save()
		return redirect('dashboard')

	# if form.is_valid():
	#     form.save()
	#     if request.user.customer:
	#         return redirect('user')
	#     else:
	#         return redirect('dashboard')
	return render(request, 'accounts/order_form.html',context)

@login_required
def delete_order(request, pk):
	orderquery = get_object_or_404(Order, id=pk)
	if request.method == 'POST':
		orderquery.delete()
		return redirect('dashboard')
	
	return render(request, 'accounts/delete_order.html', {'order': orderquery})

@login_required
def delete_all_order(request):
	orderquery = Order.objects.all()
	if request.method == 'POST':
		orderquery.delete()
		return redirect('dashboard')
	
	return render(request, 'accounts/delete_order.html', {'order': orderquery})

def UserPage(request):
	
	form = OrderSearchForm(request.POST or None)
	# total_orders = request.user.customer.order_set.all().order_by('-date_created')
	orders = request.user.customer.order_set.filter(date_created__date=date.today()).order_by('-date_created')
	orders_count = orders.count()
	context = {
		'customer': request.user, 
		'orders': orders, 
		'orders_count':orders_count, 
		'form': form,
		'p_orders': orders.filter(status="Pending").count(),
		'd_orders': orders.filter(status="Delivered").count()
		}
	
	if request.method == 'POST':
		
		orders = request.user.customer.order_set.filter(
			# item_id = form['item'].value(),
			name__icontains = form['name'].value(),
			status__icontains = form['status'].value(),
			)
		context = {
			'customer': request.user, 
			'orders': orders, 
			'orders_count':orders_count, 
			'form': form,
			'p_orders': orders.filter(status="Pending").count(),
			'd_orders': orders.filter(status="Delivered").count()
			}
	return render(request, 'accounts/user.html', context)

def all_orders(request):
	form = OrderSearchForm(request.POST or None)
	orders = Order.objects.all().order_by('-date_created')
	
	context = {
		# 'customer': request.user, 
		'orders': orders, 
		# 'cus_orders':orders.filter(customer=request.user.customer),
		'form': form,
		}
	
	if request.method == 'POST':   	
		orders = Order.objects.filter(
			# item_id = form['item'].value(),
			name__icontains = form['name'].value(),
			status__icontains = form['status'].value(),
		)
		context = {
			# 'customer': request.user, 
			
			'orders': orders, 
			'form': form,
			}
	   
	return render(request, 'accounts/all_orders.html', context)
	

# def

# todays orders
#   orders = customer.order_set.filter(date_created__lte=datetime.date.today()) : <=
#   orders = customer.order_set.filter(date_created__gte=datetime.date.today()): >=

# 5 orders (1st 5 objects)
# Entry.objects.all()[:5]