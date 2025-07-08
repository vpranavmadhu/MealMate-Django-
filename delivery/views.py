from django.shortcuts import render ,redirect, get_object_or_404
from django.http import HttpResponse
from delivery.models import Customer, Restaurant, Menu, Cart,CartItem, Order
from delivery.forms import ResForm, MenuForm
import razorpay
from django.conf import settings 
# Create your views here.

 # restaurant   
def add_res(request):
    form = ResForm(request.POST or None)
    if form.is_valid():
        res_name = request.POST.get('res_name')
        try :
            res = Restaurant.objects.get(res_name = res_name)
            return render(request, 'delivery/add_res.html', {'form': form, 'error': 'data already founded'})

        except:
            form.save()
            return redirect('users:admin_home')
    return render(request, 'delivery/add_res.html', {'form': form})

def edit_res(request,id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    if request.method == "POST":
        form = ResForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('users:admin_home')
    else:
        form = ResForm(instance=restaurant)

    return render(request, 'delivery/edit_res.html', {'form': form})

def delete_res(request,id):
    res = Restaurant.objects.get(pk = id)
    res.delete()
    return redirect("users:admin_home")

# menu
def view_menu(request,id):
    res = Restaurant.objects.get(pk=id)
    menu = Menu.objects.filter(res = res)
    return render(request, 'delivery/menu.html', {'res': res, 'menu':menu})

def add_menu(request):
    form = MenuForm(request.POST or None)
    if form.is_valid():
        menu = form.save()
        id = menu.res.id #used to get id from form
        return redirect('delivery:view_menu',id)
    return render(request,'delivery/add_menu.html', {'form': form})

def edit_menu(request,id):
    menu = get_object_or_404(Menu,pk=id)
    res_id = menu.res.id
    if request.method == "POST":
        form = MenuForm(request.POST,instance=menu)
        form.save()
        return redirect('delivery:view_menu', id=res_id)
    else:
        form = MenuForm(instance=menu)
    return render(request, 'delivery/edit_menu.html',{'form': form})

def delete_menu(request,id):
    item = Menu.objects.get(pk = id)
    res_id = item.res.id
    item.delete()
    return redirect('delivery:view_menu', res_id)

def view_cusmenu(request,id,username):
    res = Restaurant.objects.get(pk=id)
    menu = Menu.objects.filter(res = res)
    return render(request, 'delivery/cusmenu.html', {'res': res, 'menu':menu, 'username':username})

# cart
def view_cart(request,username):
    customer = Customer.objects.get(username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.cart_items.select_related('item') if cart else []

    total_price = cart.total_price() if cart else 0
    if total_price > 0:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order_data = {
            'amount': int(total_price * 100),  # amount in paisa
            'currency': 'INR',
            'payment_capture': '1'
        }
        order = client.order.create(data=order_data)
        razorpay_order_id = order['id']

        # Save order(pending order)
        order = Order.objects.create(
            customer=customer,
            total_price=total_price,
            razorpay_order_id=razorpay_order_id,
            status='pending'
        )
        
        menu_items = [ci.item for ci in cart_items]
        order.items.set(menu_items)
        order.save()

    else:
        razorpay_order_id = None

     

    return render(request, 'delivery/cart.html', {
        'username': username,
        'items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': razorpay_order_id,
    })

def add_to_cart(request,username,menuid):
    customer = Customer.objects.get(username=username)
    item = Menu.objects.get(pk=menuid)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity +=1
    cart_item.save()
    
   
    return redirect('delivery:view_cusmenu', id=item.res.id, username=username)

def cart_quantity(request,id,op):
    item = get_object_or_404(CartItem,id=id)
    username = item.cart.customer.username
    if op == '+':
        item.quantity +=1
        item.save()
        return redirect('delivery:view_cart', username=username)
    else:
        if item.quantity > 1:
            item.quantity -=1
            item.save()
        else:
            item.delete()
        return redirect('delivery:view_cart', username=username)



# order
def ordersucess(request, username):
    customer = Customer.objects.get(username = username)
    cart = Cart.objects.filter(customer = customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    order = Order.objects.filter(customer=customer).last()
    if order:
        order.status = 'completed'
        order.save()

        

    if cart:
        cart.items.clear()

    return render(request, 'delivery/ordersucess.html', {
        'username':username,
        'cart_items':cart_items,
        'total_price':total_price,
        'customer':customer
})

def orders(request,username):
    customer = Customer.objects.get(username=username)
    li = Order.objects.filter(customer=customer, status='completed').order_by('-order_on')


    return render(request,'delivery/orders.html', {'li': li, 'username': username})    