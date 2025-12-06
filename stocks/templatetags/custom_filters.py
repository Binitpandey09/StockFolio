from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def div(value, arg):
    try:
        arg_float = float(arg)
        if arg_float == 0:
            return 0
        return float(value) / arg_float
    except (ValueError, TypeError):
        return 0

@register.filter
def short_name(value):
    """
    Extract short company name from full name
    Examples:
    - "Apple Inc." -> "Apple"
    - "Tesla, Inc." -> "Tesla"
    - "NVIDIA Corporation" -> "NVIDIA"
    - "Bank of America Corporation" -> "Bank of America"
    """
    if not value:
        return value
    
    # Remove common suffixes
    suffixes = [
        ', Inc.', ' Inc.', ', Inc', ' Inc',
        ' Corporation', ' Corp.', ' Corp',
        ' Company', ' Co.', ' Co',
        ' Limited', ' Ltd.', ' Ltd',
        ' Incorporated', ' plc', ' PLC',
        ' Group', ' Holdings'
    ]
    
    result = value
    for suffix in suffixes:
        if result.endswith(suffix):
            result = result[:-len(suffix)].strip()
            break
    
    return result

@register.filter
def format_market_cap(value):
    """
    Format market cap to readable format
    Examples:
    - 1000000000 -> "1.0B"
    - 1500000000000 -> "1.5T"
    - 500000000 -> "500.0M"
    """
    try:
        value = float(value)
        if value >= 1_000_000_000_000:  # Trillion
            return f"${value / 1_000_000_000_000:.1f}T"
        elif value >= 1_000_000_000:  # Billion
            return f"${value / 1_000_000_000:.1f}B"
        elif value >= 1_000_000:  # Million
            return f"${value / 1_000_000:.1f}M"
        else:
            return f"${value:,.0f}"
    except (ValueError, TypeError):
        return "N/A"

@register.filter
def format_volume(value):
    """
    Format volume to readable format
    Examples:
    - 1000000 -> "1.0M"
    - 1500000000 -> "1.5B"
    """
    try:
        value = float(value)
        if value >= 1_000_000_000:  # Billion
            return f"{value / 1_000_000_000:.1f}B"
        elif value >= 1_000_000:  # Million
            return f"{value / 1_000_000:.1f}M"
        elif value >= 1_000:  # Thousand
            return f"{value / 1_000:.1f}K"
        else:
            return f"{value:,.0f}"
    except (ValueError, TypeError):
        return "N/A"

@register.filter
def abs_value(value):
    """Return absolute value"""
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        return 0

@register.filter
def format_percent(value):
    """Format percentage with sign"""
    try:
        value = float(value)
        if value > 0:
            return f"+{value:.2f}%"
        else:
            return f"{value:.2f}%"
    except (ValueError, TypeError):
        return "0.00%"
