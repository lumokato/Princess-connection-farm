from typing import TYPE_CHECKING, Union, Type

from core.constant import FIGHT_BTN, MAIN_BTN, DXC_ELEMENT
from scenes.fight.fighting_base import FightingBase, FightingWinBase, FightingLoseBase
from scenes.scene_base import PCRMsgBoxBase, PossibleSceneList

if TYPE_CHECKING:
    from scenes.zhuxian.zhuxian_normal import ZhuXianNormal
    from scenes.zhuxian.zhuxian_hard import ZhuXianHard


class FightingZhuXian(FightingBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_name = "FightingZhuXian"
        self.feature = self.fun_feature_exist(FIGHT_BTN["fighting_caidan"])

    def set_auto(self, auto, screen=None, max_retry=3):
        self._a.set_fight_auto(auto, screen, max_retry)

    def set_speed(self, level, max_level=1, screen=None, max_retry=3):
        self._a.set_fight_speed(level, max_level, screen, max_retry)

    def get_during(self) -> "DuringFightingZhuXian":
        return DuringFightingZhuXian(self._a)


class DuringFightingZhuXian(PossibleSceneList):
    def __init__(self, a, *args, **kwargs):
        self.LoveUpScene = LoveUpScene
        self.FightingWinZhuXian = FightingWinZhuXian
        self.FightingLoseZhuXian = FightingLoseZhuXian
        self.FightingDialog = FightingDialog
        scene_list = [
            LoveUpScene(a),
            FightingWinZhuXian(a),
            FightingLoseZhuXian(a),
            FightingDialog(a),
        ]
        super().__init__(a, scene_list, double_check=0)


class LoveUpScene(FightingWinBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_name = "LoveUpScene"
        self.feature = self.fun_feature_exist(MAIN_BTN["tiaoguo"])

    def skip(self):
        self.exit(self.click(MAIN_BTN["tiaoguo"]), interval=1)


class FightingDialog(PCRMsgBoxBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_name = "LoveUpScene"
        self.feature = self.dialog_feature

    def dialog_feature(self, screen):
        return self._a.is_exists(MAIN_BTN["speaker_box"], screen=screen, method="sq", threshold=0.95)

    def skip(self):
        self.exit(self.fun_click(1, 1), interval=0.2)


class FightingWinZhuXian(FightingWinBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_name = "FightingWinZhuXian"
        self.feature = self.win_feature

    def win_feature(self, screen):
        from core.constant import p
        duiwu_icon = p(img="img/fight/duiwu_icon.bmp", at=(896, 78, 924, 97))
        shbg = p(850, 37, img="img/fight/shbg.bmp", at=(814, 26, 886, 48))
        return self.is_exists(duiwu_icon, screen=screen) and self.is_exists(shbg, screen=screen)

    def get_star(self, screen=None):
        return self._a.get_fight_middle_stars(screen)

    def next(self):
        self.exit(self.fun_click(835, 499, post_delay=2))

    def get_after(self):
        return AfterFightingWin(self._a)


class AfterFightingWin(PossibleSceneList):
    from scenes.zhuxian.zhuxian_msg import XianDingShangDianBox, LevelUpBox, TuanDuiZhanBox, ChaoChuShangXianBox
    def __init__(self, a, *args, **kwargs):
        self.AfterFightKKR = AfterFightKKR
        self.FightingWinZhuXian2 = FightingWinZhuXian2
        scene_list = [
            self.XianDingShangDianBox(a),
            self.LevelUpBox(a),
            self.TuanDuiZhanBox(a),
            self.ChaoChuShangXianBox(a),
            FightingWinZhuXian2(a),
            AfterFightKKR(a),  # kkr剧情跳脸
        ]
        super().__init__(a, scene_list, double_check=3)


class AfterFightKKR(PCRMsgBoxBase):
    def __init__(self, a, *args, **kwargs):
        super().__init__(a)
        self.scene_name = "AfterFightKKR"
        self.feature = self.girls_feature

    def girls_feature(self, screen):
        return self.is_exists(DXC_ELEMENT["dxc_kkr"], screen=screen)

    def skip(self):
        self.chulijiaocheng(None)


class FightingWinZhuXian2(FightingWinBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_name = "FightingWinZhuXian2"
        self.feature = self.win_feature

    def win_feature(self, screen):
        from core.constant import p
        huodedaoju = p(img="img/fight/huodedaoju.bmp", at=(442, 135, 514, 160))
        xiayibu = p(img="img/fight/xiayibu.bmp", at=(794, 475, 864, 502))
        return self.is_exists(huodedaoju, screen=screen) and self.is_exists(xiayibu, screen=screen)

    def next(self):
        self.click(829, 485, post_delay=1)


class FightingLoseZhuXian(FightingLoseBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_name = "FightingLoseZhuXian2"
        self.feature = self.lose_feature

    def lose_feature(self, screen):
        from core.constant import p
        duiwu_icon = p(910, 35, img="img/fight/duiwu_icon.bmp", at=(896, 25, 924, 44))
        shbg = p(790, 37, img="img/fight/shbg.bmp", at=(754, 26, 826, 48))
        return self.is_exists(duiwu_icon, screen=screen) and self.is_exists(shbg, screen=screen)

    def goto_zhuxian(self, zhuxian_type: Union[Type["ZhuXianHard"], Type["ZhuXianNormal"]]) -> Union[
        "ZhuXianHard", "ZhuXianNormal"]:
        return self.goto(zhuxian_type, self.fun_click(814, 493))  # 前往主线关卡
