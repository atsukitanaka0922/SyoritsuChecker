import json
import os
from datetime import datetime

class LeagueStorage:
    def __init__(self, directory="data"):
        """
        リーグ情報の保存・読み込みを管理するクラス
        
        Args:
            directory (str): データを保存するディレクトリ
        """
        self.directory = directory
        # ディレクトリが存在しない場合は作成
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def save_league(self, league):
        """
        リーグ情報をJSONファイルに保存
        
        Args:
            league (League): 保存するリーグオブジェクト
            
        Returns:
            bool: 保存に成功したらTrue
        """
        try:
            # リーグ基本情報
            league_data = {
                "name": league.name,
                "current_round": league.current_round,
                "teams": [],
                "matches": []
            }
            
            # チーム情報の保存
            for team in league.teams.values():
                team_data = {
                    "id": team.id,
                    "name": team.name,
                    "matches_played": team.matches_played,
                    "wins": team.wins,
                    "losses": team.losses,
                    "draws": team.draws,
                    "goals_for": team.goals_for,
                    "goals_against": team.goals_against,
                    "players": []
                }
                
                # チームに所属する選手情報の保存
                for player in team.players.values():
                    player_data = {
                        "id": player.id,
                        "name": player.name,
                        "team_id": player.team_id,
                        "position": player.position,
                        "age": player.age,
                        "matches_played": player.matches_played,
                        "wins": player.wins,
                        "losses": player.losses,
                        "draws": player.draws
                    }
                    team_data["players"].append(player_data)
                
                league_data["teams"].append(team_data)
            
            # 試合情報の保存
            for match in league.matches:
                match_data = {
                    "home_team_id": match.home_team.id,
                    "away_team_id": match.away_team.id,
                    "date": match.date.strftime("%Y-%m-%d %H:%M:%S"),
                    "round_number": match.round_number,
                    "home_score": match.home_score,
                    "away_score": match.away_score,
                    "is_finished": match.is_finished,
                    "player_results": match.player_results
                }
                league_data["matches"].append(match_data)
            
            # ファイルに保存
            filename = os.path.join(self.directory, f"{league.name.replace(' ', '_')}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(league_data, f, ensure_ascii=False, indent=2)
            
            return True
        
        except Exception as e:
            print(f"保存中にエラーが発生しました: {e}")
            return False
    
    def load_league(self, filename):
        """
        JSONファイルからリーグ情報を読み込む
        
        Args:
            filename (str): 読み込むJSONファイル名
            
        Returns:
            League: 読み込んだリーグオブジェクト、失敗時はNone
        """
        try:
            from player_class import Player
            from team_class import Team
            from match_class import Match
            from league_class import League
            
            # ファイルパスの処理
            if not filename.endswith('.json'):
                filename += '.json'
            
            filepath = os.path.join(self.directory, filename)
            
            # ファイルが存在しない場合
            if not os.path.exists(filepath):
                print(f"ファイル '{filepath}' が見つかりません。")
                return None
            
            # JSONファイルの読み込み
            with open(filepath, 'r', encoding='utf-8') as f:
                league_data = json.load(f)
            
            # リーグオブジェクトの作成
            league = League(league_data["name"])
            league.current_round = league_data["current_round"]
            
            # チーム情報の復元
            for team_data in league_data["teams"]:
                team = Team(team_data["id"], team_data["name"])
                
                # チームの成績復元
                team.matches_played = team_data["matches_played"]
                team.wins = team_data["wins"]
                team.losses = team_data["losses"]
                team.draws = team_data["draws"]
                team.goals_for = team_data["goals_for"]
                team.goals_against = team_data["goals_against"]
                
                # 選手情報の復元
                for player_data in team_data["players"]:
                    player = Player(
                        player_data["id"],
                        player_data["name"],
                        player_data["team_id"],
                        player_data["position"],
                        player_data["age"]
                    )
                    
                    # 選手の成績復元
                    player.matches_played = player_data["matches_played"]
                    player.wins = player_data["wins"]
                    player.losses = player_data["losses"]
                    player.draws = player_data["draws"]
                    
                    team.add_player(player)
                
                league.add_team(team)
            
            # 試合情報の復元
            for match_data in league_data["matches"]:
                home_team = league.get_team(match_data["home_team_id"])
                away_team = league.get_team(match_data["away_team_id"])
                
                if home_team and away_team:
                    # 試合オブジェクトの作成
                    match_date = datetime.strptime(match_data["date"], "%Y-%m-%d %H:%M:%S")
                    match = Match(home_team, away_team, match_date, match_data["round_number"])
                    
                    # 試合結果の復元
                    if match_data["is_finished"]:
                        # スコアの設定だけで、チーム成績は更新しない（すでに復元済み）
                        match.home_score = match_data["home_score"]
                        match.away_score = match_data["away_score"]
                        match.is_finished = True
                    
                    # 選手の試合結果の復元
                    match.player_results = match_data["player_results"]
                    
                    # リーグに試合を追加
                    league.matches.append(match)
            
            return league
        
        except Exception as e:
            print(f"読み込み中にエラーが発生しました: {e}")
            return None
    
    def get_available_leagues(self):
        """
        利用可能なリーグファイルの一覧を取得
        
        Returns:
            list: 保存されているリーグファイル名のリスト
        """
        try:
            files = [f for f in os.listdir(self.directory) if f.endswith('.json')]
            # ファイル名から拡張子を除去
            leagues = [os.path.splitext(f)[0] for f in files]
            return leagues
        except Exception as e:
            print(f"リーグファイル一覧の取得中にエラーが発生しました: {e}")
            return []