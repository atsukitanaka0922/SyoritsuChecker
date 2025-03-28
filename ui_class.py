import os
import re
from team_class import Team
from player_class import Player
from match_class import Match

class LeagueUI:
    def __init__(self, league):
        """
        リーグのコンソールUI
        
        Args:
            league (League): 管理対象のリーグ
        """
        self.league = league
    
    def clear_screen(self):
        """
        画面をクリア
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """
        ヘッダーを表示
        
        Args:
            title (str): 表示するタイトル
        """
        self.clear_screen()
        print("=" * 50)
        print(f" {title}")
        print("=" * 50)
        print()
    
    def main_menu(self):
        """
        メインメニューを表示
        
        Returns:
            str: 選択されたコマンド
        """
        self.print_header(f"{self.league.name} 管理システム")
        
        print("1. チーム管理")
        print("2. 選手管理")
        print("3. 試合管理")
        print("4. 成績表示")
        print("5. ファイル操作")  # 新しいメニュー項目
        print("0. 終了")
        print()
        
        return input("コマンドを選択してください: ")
    
    # チーム管理メニューとその関連機能
    def team_menu(self):
        """
        チーム管理メニュー
        """
        while True:
            self.print_header("チーム管理")
            
            print("1. チーム一覧")
            print("2. チーム追加")
            print("3. チーム詳細")
            print("0. メインメニューに戻る")
            print()
            
            command = input("コマンドを選択してください: ")
            
            if command == "1":
                self.list_teams()
            elif command == "2":
                self.add_team()
            elif command == "3":
                self.show_team_details()
            elif command == "0":
                break
            else:
                input("無効なコマンドです。Enterキーを押してください...")
    
    def list_teams(self):
        """
        チーム一覧の表示
        """
        self.print_header("チーム一覧")
        
        if not self.league.teams:
            print("チームが登録されていません。")
        else:
            for i, team in enumerate(self.league.teams.values(), 1):
                print(f"{i}. {team.name} ({len(team.players)}人)")
        
        print()
        input("Enterキーを押してください...")
    
    def add_team(self):
        """
        チームの追加
        """
        self.print_header("チーム追加")
        
        team_name = input("チーム名を入力してください: ").strip()
        if not team_name:
            print("チーム名が入力されていません。")
            input("Enterキーを押してください...")
            return
        
        # チームIDはチーム名のアルファベット部分から生成
        team_id = re.sub(r'[^a-zA-Z]', '', team_name).lower()
        if not team_id:
            team_id = f"team{len(self.league.teams) + 1}"
        
        team = Team(team_id, team_name)
        self.league.add_team(team)
        
        print(f"チーム「{team_name}」(ID: {team_id})を追加しました。")
        input("Enterキーを押してください...")
    
    def show_team_details(self):
        """
        チーム詳細の表示
        """
        self.print_header("チーム詳細")
        
        team_name = input("チーム名を入力してください: ").strip()
        team = self.league.get_team_by_name(team_name)
        
        if not team:
            print(f"チーム「{team_name}」は見つかりません。")
            input("Enterキーを押してください...")
            return
        
        print(team)
        print("\n選手一覧:")
        if not team.players:
            print("  登録選手がいません。")
        else:
            for i, player in enumerate(team.players.values(), 1):
                print(f"  {i}. {player.name} - 勝率: {player.win_rate():.3f} ({player.wins}勝{player.losses}敗{player.draws}引分)")
        
        print()
        input("Enterキーを押してください...")
    
    # 選手管理メニューとその関連機能
    def player_menu(self):
        """
        選手管理メニュー
        """
        while True:
            self.print_header("選手管理")
            
            print("1. 選手一覧")
            print("2. 選手追加")
            print("3. 選手詳細")
            print("0. メインメニューに戻る")
            print()
            
            command = input("コマンドを選択してください: ")
            
            if command == "1":
                self.list_players()
            elif command == "2":
                self.add_player()
            elif command == "3":
                self.show_player_details()
            elif command == "0":
                break
            else:
                input("無効なコマンドです。Enterキーを押してください...")
    
    def list_players(self):
        """
        選手一覧の表示
        """
        self.print_header("選手一覧")
        
        all_players = []
        for team in self.league.teams.values():
            for player in team.players.values():
                all_players.append((player, team.name))
        
        if not all_players:
            print("選手が登録されていません。")
        else:
            for i, (player, team_name) in enumerate(all_players, 1):
                print(f"{i}. {player.name} ({team_name})")
        
        print()
        input("Enterキーを押してください...")
    
    def add_player(self):
        """
        選手の追加
        """
        self.print_header("選手追加")
        
        team_name = input("所属チーム名を入力してください: ").strip()
        team = self.league.get_team_by_name(team_name)
        
        if not team:
            print(f"チーム「{team_name}」は見つかりません。")
            input("Enterキーを押してください...")
            return
        
        player_name = input("選手名を入力してください: ").strip()
        if not player_name:
            print("選手名が入力されていません。")
            input("Enterキーを押してください...")
            return
        
        position = input("ポジションを入力してください（任意）: ").strip()
        
        age_str = input("年齢を入力してください（任意）: ").strip()
        age = int(age_str) if age_str.isdigit() else None
        
        # 選手IDは選手名のアルファベット部分から生成
        player_id = re.sub(r'[^a-zA-Z]', '', player_name).lower()
        if not player_id:
            player_id = f"player{len(team.players) + 1}"
        
        player = Player(player_id, player_name, team.id, position, age)
        team.add_player(player)
        
        print(f"選手「{player_name}」をチーム「{team_name}」に追加しました。")
        input("Enterキーを押してください...")
    
    def show_player_details(self):
        """
        選手詳細の表示
        """
        self.print_header("選手詳細")
        
        player_name = input("選手名を入力してください: ").strip()
        
        found_player = None
        team_name = None
        
        for team in self.league.teams.values():
            for player in team.players.values():
                if player.name == player_name:
                    found_player = player
                    team_name = team.name
                    break
            if found_player:
                break
        
        if not found_player:
            print(f"選手「{player_name}」は見つかりません。")
            input("Enterキーを押してください...")
            return
        
        print(f"チーム: {team_name}")
        print(found_player)
        
        print()
        input("Enterキーを押してください...")
    
    # 試合管理メニューとその関連機能
    def match_menu(self):
        """
        試合管理メニュー
        """
        while True:
            self.print_header("試合管理")
            
            print("1. 試合一覧")
            print("2. 試合追加")
            print("3. スコア入力（数値）")
            print("4. 勝敗入力（○×）")
            print("5. 選手成績入力")
            print("6. 次のラウンドへ")
            print("0. メインメニューに戻る")
            print()
            
            command = input("コマンドを選択してください: ")
            
            if command == "1":
                self.list_matches()
            elif command == "2":
                self.add_match()
            elif command == "3":
                self.enter_match_score()
            elif command == "4":
                self.enter_match_result()
            elif command == "5":
                self.enter_player_results()
            elif command == "6":
                self.next_round()
            elif command == "0":
                break
            else:
                input("無効なコマンドです。Enterキーを押してください...")
    
    def list_matches(self):
        """
        試合一覧の表示
        """
        self.print_header("試合一覧")
        
        if not self.league.matches:
            print("試合が登録されていません。")
        else:
            for i, match in enumerate(self.league.matches, 1):
                print(f"{i}. {match}")
        
        print()
        input("Enterキーを押してください...")
    
    def add_match(self):
        """
        試合の追加
        """
        self.print_header("試合追加")
        
        home_team_name = input("ホームチーム名を入力してください: ").strip()
        away_team_name = input("アウェイチーム名を入力してください: ").strip()
        
        home_team = self.league.get_team_by_name(home_team_name)
        away_team = self.league.get_team_by_name(away_team_name)
        
        if not home_team:
            print(f"チーム「{home_team_name}」は見つかりません。")
            input("Enterキーを押してください...")
            return
        
        if not away_team:
            print(f"チーム「{away_team_name}」は見つかりません。")
            input("Enterキーを押してください...")
            return
        
        if home_team.id == away_team.id:
            print("同じチーム同士の試合は登録できません。")
            input("Enterキーを押してください...")
            return
        
        match = Match(home_team, away_team, round_number=self.league.current_round)
        self.league.matches.append(match)
        
        print(f"Round {self.league.current_round}: {home_team.name} vs {away_team.name} の試合を追加しました。")
        input("Enterキーを押してください...")
    
    def enter_match_score(self):
        """
        試合スコアの入力（数値）
        """
        self.print_header("スコア入力（数値）")
        
        if not self.league.matches:
            print("試合が登録されていません。")
            input("Enterキーを押してください...")
            return
        
        # 未完了の試合のみ表示
        unfinished_matches = [m for m in self.league.matches if not m.is_finished]
        if not unfinished_matches:
            print("すべての試合が終了しています。")
            input("Enterキーを押してください...")
            return
        
        print("スコアを入力する試合を選んでください:")
        for i, match in enumerate(unfinished_matches, 1):
            print(f"{i}. {match}")
        
        try:
            match_idx = int(input("\n番号を入力: ")) - 1
            if match_idx < 0 or match_idx >= len(unfinished_matches):
                print("無効な番号です。")
                input("Enterキーを押してください...")
                return
        except ValueError:
            print("数値を入力してください。")
            input("Enterキーを押してください...")
            return
        
        match = unfinished_matches[match_idx]
        
        try:
            home_score = int(input(f"{match.home_team.name}のスコア: "))
            away_score = int(input(f"{match.away_team.name}のスコア: "))
            
            if home_score < 0 or away_score < 0:
                print("スコアは0以上の整数を入力してください。")
                input("Enterキーを押してください...")
                return
            
            match.set_score(home_score, away_score)
            print(f"スコアを登録しました: {match.home_team.name} {home_score}-{away_score} {match.away_team.name}")
            input("Enterキーを押してください...")
        except ValueError:
            print("数値を入力してください。")
            input("Enterキーを押してください...")
    
    def enter_match_result(self):
        """
        試合勝敗の入力（○×）
        """
        self.print_header("勝敗入力（○×）")
        
        if not self.league.matches:
            print("試合が登録されていません。")
            input("Enterキーを押してください...")
            return
        
        # 未完了の試合のみ表示
        unfinished_matches = [m for m in self.league.matches if not m.is_finished]
        if not unfinished_matches:
            print("すべての試合が終了しています。")
            input("Enterキーを押してください...")
            return
        
        print("勝敗を入力する試合を選んでください:")
        for i, match in enumerate(unfinished_matches, 1):
            print(f"{i}. {match}")
        
        try:
            match_idx = int(input("\n番号を入力: ")) - 1
            if match_idx < 0 or match_idx >= len(unfinished_matches):
                print("無効な番号です。")
                input("Enterキーを押してください...")
                return
        except ValueError:
            print("数値を入力してください。")
            input("Enterキーを押してください...")
            return
        
        match = unfinished_matches[match_idx]
        
        print(f"\n{match.home_team.name} vs {match.away_team.name}")
        print("勝敗を ○-× (ホームの勝ち), ×-○ (アウェイの勝ち), △-△ (引き分け) の形式で入力してください。")
        
        result_symbol = input("勝敗: ")
        
        if match.set_score_by_symbols(result_symbol):
            print(f"勝敗を登録しました: {match.home_team.name} {result_symbol} {match.away_team.name}")
        else:
            print("無効な勝敗形式です。")
        
        input("Enterキーを押してください...")
    
    def enter_player_results(self):
        """
        選手個人の成績入力
        """
        self.print_header("選手成績入力")
        
        if not self.league.matches:
            print("試合が登録されていません。")
            input("Enterキーを押してください...")
            return
        
        # 完了済みの試合のみ表示
        finished_matches = [m for m in self.league.matches if m.is_finished]
        if not finished_matches:
            print("完了した試合がありません。")
            input("Enterキーを押してください...")
            return
        
        print("選手成績を入力する試合を選んでください:")
        for i, match in enumerate(finished_matches, 1):
            print(f"{i}. {match}")
        
        try:
            match_idx = int(input("\n番号を入力: ")) - 1
            if match_idx < 0 or match_idx >= len(finished_matches):
                print("無効な番号です。")
                input("Enterキーを押してください...")
                return
        except ValueError:
            print("数値を入力してください。")
            input("Enterキーを押してください...")
            return
        
        match = finished_matches[match_idx]
        
        print(f"\n{match.home_team.name} {match.home_score}-{match.away_score} {match.away_team.name}")
        
        team_choice = input("どちらのチームの選手成績を入力しますか？ (1: ホーム, 2: アウェイ): ")
        
        if team_choice not in ["1", "2"]:
            print("1または2を入力してください。")
            input("Enterキーを押してください...")
            return
        
        team = match.home_team if team_choice == "1" else match.away_team
        
        if not team.players:
            print(f"{team.name}に選手が登録されていません。")
            input("Enterキーを押してください...")
            return
        
        print(f"\n{team.name}の選手一覧:")
        players_list = list(team.players.values())
        for i, player in enumerate(players_list, 1):
            print(f"{i}. {player.name}")
        
        try:
            player_idx = int(input("\n選手番号を入力: ")) - 1
            if player_idx < 0 or player_idx >= len(players_list):
                print("無効な番号です。")
                input("Enterキーを押してください...")
                return
        except ValueError:
            print("数値を入力してください。")
            input("Enterキーを押してください...")
            return
        
        player = players_list[player_idx]
        
        print("\n選手の成績を ○ (勝ち), × (負け), △ (引き分け) で入力してください。")
        result = input(f"{player.name}の成績: ")
        
        if result not in ["○", "×", "△"]:
            print("○, ×, △ のいずれかを入力してください。")
            input("Enterキーを押してください...")
            return
        
        match.add_player_result(player.id, result)
        print(f"{player.name}の成績を {result} として登録しました。")
        input("Enterキーを押してください...")
    
    def next_round(self):
        """
        次のラウンドに進む
        """
        self.print_header("次のラウンドへ")
        
        current_round = self.league.current_round
        
        # 現在のラウンドの試合がすべて終了しているか確認
        current_round_matches = [m for m in self.league.matches if m.round_number == current_round]
        unfinished_matches = [m for m in current_round_matches if not m.is_finished]
        
        if unfinished_matches:
            print(f"Round {current_round}の試合がまだ終了していません。")
            for match in unfinished_matches:
                print(f"- {match}")
            
            print("\n全ての試合を終了させてから次のラウンドに進んでください。")
            input("Enterキーを押してください...")
            return
        
        self.league.next_round()
        print(f"Round {current_round}から Round {self.league.current_round} に進みました。")
        input("Enterキーを押してください...")
    
    # 成績表示メニューとその関連機能
    def stats_menu(self):
        """
        成績表示メニュー
        """
        while True:
            self.print_header("成績表示")
            
            print("1. チーム順位表")
            print("2. 選手勝率ランキング")
            print("0. メインメニューに戻る")
            print()
            
            command = input("コマンドを選択してください: ")
            
            if command == "1":
                self.show_team_standings()
            elif command == "2":
                self.show_player_rankings()
            elif command == "0":
                break
            else:
                input("無効なコマンドです。Enterキーを押してください...")
    
    def show_team_standings(self):
        """
        チーム順位表の表示
        """
        self.print_header("チーム順位表")
        
        standings = self.league.get_standings()
        
        if not standings:
            print("チームが登録されていないか、試合が行われていません。")
            input("Enterキーを押してください...")
            return
        
        print(f"{'順位':<4} {'チーム名':<20} {'試合':<4} {'勝':<4} {'分':<4} {'負':<4} {'勝点':<4} {'勝率':<6} {'得点':<4} {'失点':<4} {'得失':<4}")
        print("-" * 80)
        
        for rank, (team, points, win_rate, goal_diff) in enumerate(standings, 1):
            print(f"{rank:<4} {team.name:<20} {team.matches_played:<4} {team.wins:<4} {team.draws:<4} "
                  f"{team.losses:<4} {points:<4} {win_rate:.3f} {team.goals_for:<4} "
                  f"{team.goals_against:<4} {goal_diff:<4}")
        
        print()
        input("Enterキーを押してください...")
    
    def show_player_rankings(self):
        """
        選手勝率ランキングの表示
        """
        self.print_header("選手勝率ランキング")
        
        rankings = self.league.get_player_rankings()
        
        if not rankings:
            print("選手が登録されていないか、試合が行われていません。")
            input("Enterキーを押してください...")
            return
        
        # チーム名を取得
        team_names = {}
        for team in self.league.teams.values():
            for player_id in team.players:
                team_names[player_id] = team.name
        
        print(f"{'順位':<4} {'選手名':<20} {'チーム':<15} {'試合':<4} {'勝':<4} {'分':<4} {'負':<4} {'勝率':<6}")
        print("-" * 70)
        
        for rank, (player, win_rate, matches) in enumerate(rankings, 1):
            print(f"{rank:<4} {player.name:<20} {team_names.get(player.id, ''):<15} "
                  f"{player.matches_played:<4} {player.wins:<4} {player.draws:<4} "
                  f"{player.losses:<4} {win_rate:.3f}")
        
        print()
        input("Enterキーを押してください...")
    
    # ファイル操作メニューとその関連機能
    def file_menu(self):
        """
        ファイル操作メニュー（保存/読み込み）
        """
        while True:
            self.print_header("ファイル操作")
            
            print("1. 大会データを保存")
            print("2. 大会データを読み込む")
            print("0. メインメニューに戻る")
            print()
            
            command = input("コマンドを選択してください: ")
            
            if command == "1":
                self.save_league_data()
            elif command == "2":
                self.load_league_data()
            elif command == "0":
                break
            else:
                input("無効なコマンドです。Enterキーを押してください...")

    def save_league_data(self):
        """
        リーグデータを保存
        """
        self.print_header("大会データの保存")
        
        print(f"現在の大会名: {self.league.name}")
        print(f"チーム数: {len(self.league.teams)}")
        print(f"試合数: {len(self.league.matches)}")
        print()
        
        confirm = input("この大会データを保存しますか？ (y/n): ")
        if confirm.lower() != 'y':
            print("保存をキャンセルしました。")
            input("Enterキーを押してください...")
            return
        
        # LeagueStorageを使用してデータを保存
        from league_storage import LeagueStorage
        storage = LeagueStorage()
        
        if storage.save_league(self.league):
            print(f"大会「{self.league.name}」のデータを保存しました。")
        else:
            print("保存に失敗しました。")
        
        input("Enterキーを押してください...")

    def load_league_data(self):
        """
        保存されたリーグデータを読み込む
        """
        self.print_header("大会データの読み込み")
        
        # 現在の状態で未保存のデータがある場合の確認
        if self.league.teams or self.league.matches:
            print("警告: 現在の大会データは失われます。")
            confirm = input("続行しますか？ (y/n): ")
            if confirm.lower() != 'y':
                print("読み込みをキャンセルしました。")
                input("Enterキーを押してください...")
                return
        
        # 利用可能なリーグファイル一覧を取得
        from league_storage import LeagueStorage
        storage = LeagueStorage()
        available_leagues = storage.get_available_leagues()
        
        if not available_leagues:
            print("保存されている大会データが見つかりません。")
            input("Enterキーを押してください...")
            return
        
        print("利用可能な大会データ:")
        for i, league_name in enumerate(available_leagues, 1):
            print(f"{i}. {league_name}")
        
        try:
            league_idx = int(input("\n読み込む大会の番号を入力: ")) - 1
            if league_idx < 0 or league_idx >= len(available_leagues):
                print("無効な番号です。")
                input("Enterキーを押してください...")
                return
        except ValueError:
            print("数値を入力してください。")
            input("Enterキーを押してください...")
            return
        
        selected_league = available_leagues[league_idx]
        
        # リーグデータの読み込み
        loaded_league = storage.load_league(selected_league)
        
        if loaded_league:
            self.league = loaded_league
            print(f"大会「{loaded_league.name}」のデータを読み込みました。")
            print(f"チーム数: {len(loaded_league.teams)}")
            print(f"試合数: {len(loaded_league.matches)}")
        else:
            print("読み込みに失敗しました。")
        
        input("Enterキーを押してください...")