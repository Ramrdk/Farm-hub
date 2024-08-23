from django import template

register = template.Library()

@register.filter
def cart_total(cart_items):
    return sum(float(item.total_price) for item in cart_items)




@register.filter
def mul(value, arg):
    """Multiplies the value by the argument, converting to float if necessary."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0  # Handle the error gracefully

@register.filter
def sum_total(cart_items):
    """Calculates the total price of all items in the cart."""
    total = 0
    for item in cart_items:
        total += float(item.quantity) * float(item.product.prize)
    return total
