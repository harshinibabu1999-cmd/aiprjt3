from django.db.models import Sum, Count

@login_required
def leaderboard(request):
    top_users = Result.objects.values('user__username').annotate(
        total_score=Sum('score'),
        quizzes_taken=Count('id')
    ).order_by('-total_score')[:10]
    
    return render(request, 'leaderboard.html', {'top_users': top_users})
