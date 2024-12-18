from django.db.models import F, Sum
from datetime import datetime
from datetime import timedelta
from .models import Product, OrderItem
from django.utils.timezone import now
# from django.utils.timezone import make_aware


def total_revenue_day():
    today = datetime.now().date()
    revenue = (
        OrderItem.objects.filter(timestamp__date=today)
        .annotate(revenue=F('product__price') * F('quantity'))  # Calculate revenue per item
        .aggregate(total_revenue=Sum('revenue'))['total_revenue'] or 0.0
    )
    formatted_revenue = f"{revenue:,.2f}"
    return formatted_revenue


def total_revenue_week():
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # Start of the week
    week_end = week_start + timedelta(days=6)  # End of the week

    revenue = (
        OrderItem.objects.filter(timestamp__date__range=[week_start, week_end])
        .annotate(revenue=F('product__price') * F('quantity'))
        .aggregate(total_revenue=Sum('revenue'))['total_revenue'] or 0.0
    )
    formatted_revenue = f"{revenue:,.2f}"
    return formatted_revenue


def total_revenue_month():
    today = datetime.now()
    current_month = today.month
    current_year = today.year

    revenue = (
        OrderItem.objects.filter(timestamp__month=current_month, timestamp__year=current_year)
        .annotate(revenue=F('product__price') * F('quantity'))  # Calculate revenue per item
        .aggregate(total_revenue=Sum('revenue'))['total_revenue'] or 0.0
    )
    formatted_revenue = f"{revenue:,.2f}"
    return formatted_revenue


def total_revenue_annual():
    today = datetime.now()
    current_year = today.year

    revenue = (
        OrderItem.objects.filter(timestamp__year=current_year)
        .annotate(revenue=F('product__price') * F('quantity'))  # Calculate revenue per item
        .aggregate(total_revenue=Sum('revenue'))['total_revenue'] or 0.0
    )
    formatted_revenue = f"{revenue:,.2f}"
    return formatted_revenue


def create_order_items_from_invoice(invoice_data):

    for product_id, quantity in invoice_data.items():
        product = Product.objects.get(id=product_id)

        # Create an OrderItem
        OrderItem.objects.create(
            product=product,
            quantity=quantity,
            timestamp=now(),
        )

        # Deduct from stock
        product.quantity -= quantity
        product.save()




def get_top_products_by_quantity_today():
    today = datetime.now().date()
    return (
        OrderItem.objects.filter(timestamp__gte=today)
        .values('product__name')  # Group by product name
        .annotate(total_quantity=Sum('quantity'))  # Sum of quantities sold
        .order_by('-total_quantity')[:5]  # Top 5 results
    )

def get_top_products_by_quantity_week():
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # Start of the week
    week_end = week_start + timedelta(days=6)

    return (
            OrderItem.objects.filter(timestamp__date__range=[week_start, week_end])
            .values('product__name')  # Group by product name
            .annotate(total_quantity=Sum('quantity'))  # Sum of quantities sold
            .order_by('-total_quantity')[:5]  # Top 5 results
        )

def get_top_products_by_quantity_month():
    today = datetime.now()
    current_month = today.month
    current_year = today.year

    return (
        OrderItem.objects.filter(timestamp__month=current_month, timestamp__year=current_year)
        .values('product__name')  # Group by product name
        .annotate(total_quantity=Sum('quantity'))  # Sum of quantities sold
        .order_by('-total_quantity')[:5]  # Top 5 results
    )


def get_top_products_by_revenue_today():
    today = datetime.now().date()
    return (
        OrderItem.objects.filter(timestamp__gte=today)
        .values('product__name')  # Group by product name
        .annotate(total_revenue=Sum(F('quantity') * F('product__price')))  # Sum of quantities sold
        .order_by('-total_revenue')[:5]  # Top 5 results
    )

def get_top_products_by_revenue_week():
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # Start of the week
    week_end = week_start + timedelta(days=6)

    return (
        OrderItem.objects.filter(timestamp__date__range=[week_start, week_end])
        .values('product__name')  # Group by product name
        .annotate(total_revenue=Sum(F('quantity') * F('product__price')))  # Sum of quantities sold
        .order_by('-total_revenue')[:5]  # Top 5 results
    )

def get_top_products_by_revenue_month():
    today = datetime.now()
    current_month = today.month
    current_year = today.year

    return (
        OrderItem.objects.filter(timestamp__month=current_month, timestamp__year=current_year)
        .values('product__name')  # Group by product name
        .annotate(total_revenue=Sum(F('quantity') * F('product__price')))  # Sum of quantities sold
        .order_by('-total_revenue')[:5]  # Top 5 results
    )











