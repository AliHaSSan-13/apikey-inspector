from rich.table import Table
from apikey_inspector.models.result import InspectionResult

def create_rich_table(result: InspectionResult) -> Table:
    """Format an InspectionResult into a rich Table."""
    table = Table(title=f"API Key Inspection: {result.provider.value.upper()}", show_header=False)
    
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Provider", result.provider.value)
    table.add_row("Key Type", result.key_type.value)
    table.add_row("Key Masked", result.key_masked)
    
    status_color = "green" if result.valid else "red" if result.status == "expired" else "yellow"
    table.add_row("Status", f"[{status_color}]{result.status.value}[/{status_color}]")
    
    if result.models:
        # truncate models to fit
        models_str = ", ".join(result.models)
        if len(models_str) > 60:
            models_str = models_str[:57] + "..."
        table.add_row("Available Models", models_str)
        
    if result.usage:
        usage = result.usage
        table.add_row("Usage This Month", str(usage.tokens_used_this_month or "N/A"))
        if usage.cost_this_month is not None:
            table.add_row("Cost This Month", f"${usage.cost_this_month:.2f}")

    if result.rate_limits:
        limits = ", ".join(f"{k}: {v}" for k, v in result.rate_limits.items())
        table.add_row("Rate Limits", limits)
        
    if result.errors:
        err_str = "\n".join(result.errors)
        table.add_row("Errors/Warnings", f"[red]{err_str}[/red]")
        
    return table
