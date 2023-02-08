rot_about_ja = """
「ROT N」はアルファベットを、ABC…の順番に沿ってN番ずらす暗号です。例えばROT 3を使用するとAはDに、BはEに変換されます。Zを超えるとAに戻ります。例えばROT 3であればYはBに移ります。

これは最もシンプルなタイプの暗号であり、特にROT 13はPythonのCODECモジュールにも組み込まれています。ROTあるいはROT13は多くの人にとって最初に知る暗号であり、暗号の基礎中の基礎としての位置にあります。

「ROT N」の暗号強度は皆無であり、単独で暗号としての用を果たすことはありません。しかしROT13は「一見して内容はわからないが、その気になれば簡単に解読できる」という特徴から、BBSでネタバレを避けたい人に配慮して発言する際やジオキャッシングでヒントを出す際などに使われるというユースケースも存在しました。

ROT Nでエンコードされた文章は、ROT -Nでデコードすることができます。アルファベットの文字数が26文字であるため、「ROT -13」は「ROT 13」と同一であり、そのためROT13でエンコードされた文章はROT13でデコードすることができます。このエンコード・デコードの向きを気にしなくていいという対象性も、上記のユースケースでROT13が好まれた理由の一つだと考えています。例えば「ROT 5です」と言われて暗号文を渡されたときに、+5したらデコードできるのか-5したらデコードできるのか迷うことがありますが、ROT13にはそういう心配がありません。

ROT暗号は古代ローマのカエサル（シーザー）が使用したという逸話から、カエサル暗号やシーザー暗号とも呼ばれます。当時でもこの方式に暗号としての十分な強度があったとは考えづらく、もう少し複雑な文脈があるか、あるいは根も葉もないか・・と個人的には考えていますが、調査するのも難しいため踏み込みません。

ROTという呼び名はアルファベットの環を回すイメージでRotateあたりの単語由来かと思われます。
"""

rot_hot_to_use_ja = """
本サイトのツールでは、入力された文章に対し、ROT 0から+25までを一覧で出力します。通常のアルファベットのみを変換の対象とし、数字や記号、他言語の文字種については入力された内容のまま出力します。

大文字で入力されたものは大文字のまま、小文字で入力されたものは小文字のままでROT変換を行います。
"""

rot_test_cases = """
<b>Case 1</b>
INPUT = ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
ROT +8
OUTPUT = IJKLMNOPQRSTUVWXYZABCDEFGHijklmnopqrstuvwxyzabcdefgh0123456789

<b>Case 2</b>
INPUT = The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well.
ROT +20
OUTPUT = Nby luvvcn-bify qyhn mnlucabn ih fcey u nohhyf zil migy qus, uhx nbyh xcjjyx moxxyhfs xiqh, mi moxxyhfs nbun Ufcwy bux hin u gigyhn ni nbche uvion mnijjcha bylmyfz vyzily mby ziohx bylmyfz zuffcha xiqh u pyls xyyj qyff.

(Can be reconciled at <a href="https://multidec.web-lab.at/mr.php" target="_blank" class="link">https://multidec.web-lab.at/mr.php</a>)

"""

rot_challenge = """
B Ebzrb, Ebzrb, jurersber neg gubh Ebzrb?
Qral gul sngure naq ershfr gul anzr.
Be vs gubh jvyg abg, or ohg fjbea zl ybir,
Naq V’yy ab ybatre or n Pnchyrg.
"""

rot_link = """
<a href="../rot" target="_blank" class="link">Cipher Tool: Rot</a>
"""


contents = {
    'rot-ja': {
        'title': 'ROT',
        'lang': 'Ja',
        'about': rot_about_ja,
        'how_to_use_tool': rot_hot_to_use_ja,
        'test_cases': rot_test_cases,
        'challenge': rot_challenge,
        'link': rot_link,
    },
    'rot-en': {
        'title': 'ROT',
        'lang': 'En',
        'about': '',
        'how_to_use_tool': '',
        'test_cases': rot_test_cases,
        'challenge': rot_challenge,
        'link': rot_link,
    },
}


def output_with_tag(text):
    text = text.strip()
    if len(text) == 0:
        return '<p>No contents yet.</p>'
    rows = text.split('\n')
    output = ''
    for row in rows:
        row = row.strip(' ')
        if len(row) == 0:
            output += '<br>'
        else:
            output += '<p>'+row+'</p>'
    return output


def prose(mode, pageid):
    if mode == 'keys':
        return contents.keys()
    else:
        content = contents[pageid]
        return {'title': content['title'],
                'lang': content['lang'],
                'about': output_with_tag(content['about']),
                'how_to_use_tool': output_with_tag(content['how_to_use_tool']),
                'test_cases': output_with_tag(content['test_cases']),
                'challenge': output_with_tag(content['challenge']),
                'link': output_with_tag(content['link']), }
