from datetime import datetime

class Match:
    def __init__(self, home_team, away_team, date=None, round_number=None):
        """
        試合情報
        
        Args:
            home_team (Team): ホームチーム
            away_team (Team): アウェイチーム
            date (datetime, optional): 試合日
            round_number (int, optional): ラウンド数
        """
        self.home_team = home_team
        self.away_team = away_team
        self.date = date if date else datetime.now()
        self.round_number = round_number
        
        # 試合結果
        self.home_score = None
        self.away_score = None
        self.is_finished = False
        
        # 選手の結果（選手ID -> 結果）
        self.player_results = {}
    
    def set_score(self, home_score, away_score):
        """
        スコアをセット
        
        Args:
            home_score (int): ホームチームの得点
            away_score (int): アウェイチームの得点
        """
        self.home_score = home_score
        self.away_score = away_score
        self.is_finished = True
        
        # チームの成績を更新
        if home_score > away_score:
            # ホームチームの勝ち
            self.home_team.add_match_result(home_score, away_score, '○')
            self.away_team.add_match_result(away_score, home_score, '×')
        elif home_score < away_score:
            # アウェイチームの勝ち
            self.home_team.add_match_result(home_score, away_score, '×')
            self.away_team.add_match_result(away_score, home_score, '○')
        else:
            # 引き分け
            self.home_team.add_match_result(home_score, away_score, '△')
            self.away_team.add_match_result(away_score, home_score, '△')
    
    def set_score_by_symbols(self, result_symbol):
        """
        記号（○×）で勝敗を設定
        
        Args:
            result_symbol (str): 例 "○-×" (ホームの勝ち) or "×-○" (アウェイの勝ち) or "△-△" (引き分け)
        
        Returns:
            bool: 設定に成功したらTrue
        """
        symbols = result_symbol.split('-')
        if len(symbols) != 2:
            return False
        
        home_symbol, away_symbol = symbols
        
        # 矛盾チェック
        if (home_symbol == '○' and away_symbol != '×') or \
           (home_symbol == '×' and away_symbol != '○') or \
           (home_symbol == '△' and away_symbol != '△'):
            return False
        
        # 仮のスコアを設定
        if home_symbol == '○':
            self.set_score(1, 0)  # ホームの勝ち
        elif home_symbol == '×':
            self.set_score(0, 1)  # アウェイの勝ち
        else:
            self.set_score(0, 0)  # 引き分け
        
        return True
    
    def add_player_result(self, player_id, result):
        """
        選手の試合結果を追加
        
        Args:
            player_id (str): 選手ID
            result (str): '○' (勝ち), '×' (負け), or '△' (引き分け)
        """
        self.player_results[player_id] = result
        
        # 選手の所属チームを特定して選手の成績も更新
        if player_id in self.home_team.players:
            self.home_team.players[player_id].add_result(result)
        elif player_id in self.away_team.players:
            self.away_team.players[player_id].add_result(result)
    
    def __str__(self):
        """
        試合情報の文字列表現
        """
        round_info = f"Round {self.round_number}: " if self.round_number else ""
        date_str = self.date.strftime("%Y-%m-%d")
        
        if self.is_finished:
            return f"{round_info}{self.home_team.name} {self.home_score}-{self.away_score} {self.away_team.name} ({date_str})"
        else:
            return f"{round_info}{self.home_team.name} vs {self.away_team.name} ({date_str})"