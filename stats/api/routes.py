from ninja_extra import NinjaExtraAPI, api_controller, http_get
from django.http import JsonResponse
from ..auth import require_auth
from ..services.valorant_api import ValorantAPI

api = NinjaExtraAPI()

@api_controller('/stats', tags=['Stats'])
class StatsController:
    
    @http_get('/matches/{name}/{tag}')
    @require_auth
    async def get_match_history(self, request, name: str, tag: str):
        """Récupère l'historique des matchs pour un joueur"""
        try:
            valorant_api = ValorantAPI(request.app.mongodb)
            matches = await valorant_api.get_match_history(name, tag)
            return matches
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    @http_get('/matches/{match_id}')
    @require_auth
    async def get_match_details(self, request, match_id: str):
        """Récupère les détails d'un match spécifique"""
        try:
            valorant_api = ValorantAPI(request.app.mongodb)
            match = await valorant_api.matches_collection.find_one({"match_id": match_id})
            if not match:
                return JsonResponse({'error': 'Match not found'}, status=404)
            return match
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
