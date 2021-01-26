try:
    from . import i18n
    from . import connect_core
    from . import screens
    from . import exceptions
    from . import command
except ModuleNotFoundError:
    import i18n
    import connect_core
    import screens
    import exceptions
    import command


def register(
        api: object,
        new_ptt_id: str,
        new_ptt_pw: str,
        are_you_18: bool,
        mood_on_demand: bool,
        nick_name: str,
        real_name: str,
        service: str,
        address: str) -> None:

    cmd_list = list()
    cmd_list.append('new')
    cmd_list.append(command.Enter)
    cmd = ''.join(cmd_list)

    target_list = [
        connect_core.TargetUnit(
            '選擇' + ('' if mood_on_demand else '不') + '看到來自其它使用者的心情點播',
            '請問您希望在動態告示區看到來自其它使用者的心情點播嗎',
            response=('y' if mood_on_demand else 'n') + command.Enter
        ),
        connect_core.TargetUnit(
            '輸入使用者代號',
            '請輸入使用者代號',
            response=new_ptt_id + command.Enter,
            max_match=1
        ),
        #
        connect_core.TargetUnit(
            '此代號已經有人使用',
            '此代號已經有人使用',
            exceptions_=exceptions.IDExist()
        ),
        connect_core.TargetUnit(
            '設定密碼',
            '請設定密碼',
            response=new_ptt_pw + command.Enter,
            max_match=1
        ),
        connect_core.TargetUnit(
            '確認密碼',
            '請確認密碼',
            response=new_ptt_pw + command.Enter,
            max_match=1
        ),
        connect_core.TargetUnit(
            '輸入綽號暱稱',
            '綽號暱稱',
            response=('' if not nick_name else nick_name) + command.Enter,
            max_match=1
        ),
        connect_core.TargetUnit(
            '輸入真實姓名',
            '真實姓名',
            response=('' if not real_name else real_name) + command.Enter,
            max_match=1
        ),
        connect_core.TargetUnit(
            '輸入服務單位',
            '服務單位',
            response=('' if not service else service) + command.Enter,
            max_match=1
        ),
        connect_core.TargetUnit(
            '輸入聯絡地址',
            '聯絡地址',
            response=('' if not address else address) + command.Enter,
            max_match=1
        ),
        connect_core.TargetUnit(
            ('年' if not are_you_18 else '未') + '滿十八歲',
            '您是否年滿十八歲並同意觀看此類看板',
            response=('y' if not are_you_18 else 'n') + command.Enter,
            max_match=1
        ),
        connect_core.TargetUnit(
            '任意鍵',
            '任意鍵',
            response=command.Space,
        ),
        connect_core.TargetUnit(
            '不使用 E-Mail 來認證',
            '是否要使用 E-Mail 來認證',
            # default enter
            response=command.Enter,
        ),
        connect_core.TargetUnit(
            '不使用 E-Mail 來認證',
            '您確定要填寫註冊單嗎',
            # default enter
            response=command.Enter,
        ),

        #
        #
        # connect_core.TargetUnit(
        #     [
        #         i18n.bucket,
        #         i18n.Success,
        #     ],
        #     '其它鍵結束',
        #     response=command.Enter,
        # ),
        # connect_core.TargetUnit(
        #     [
        #         i18n.bucket,
        #         i18n.Success,
        #     ],
        #     '權限設定系統',
        #     response=command.Enter,
        # ),

        # connect_core.TargetUnit(
        #     [
        #         i18n.bucket,
        #         i18n.Success,
        #     ],
        #     screens.Target.InBoard,
        #     break_detect=True
        # ),
    ]

    api.connect_core.send(
        cmd,
        target_list
    )

    last_screen = api.connect_core.get_screen_queue()[-1]
