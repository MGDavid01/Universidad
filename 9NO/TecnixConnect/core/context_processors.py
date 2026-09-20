def nav_context(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {"nav_role": None}
    return {
        "nav_role": user.role,
        "nav_org": user.organization,
    }
