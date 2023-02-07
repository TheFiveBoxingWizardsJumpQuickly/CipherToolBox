contents = {
    'rot-ja': {
        'title': 'ROT',
        'about':
        """
        最もシンプルなタイプの暗号で、特にROT 13はPythonのCODECモジュールにも組み込まれているなど、最初に知る暗号、暗号の基礎の基礎としての王様の位置にあると思います。
        暗号強度は皆無で、これ単品でなんら暗号としての用を果たすことはありません。しかしROT13は「一見して内容はわからないが、その気になれば簡単に解読できる」という特徴から、BBSでネタバレを避けたい人に配慮して発言する際やジオキャッシングでヒントを出す際などに使われるというユースケースも存在しました。

        ROT NでN番先に進めた暗号のデコードは、ROT -Nとなります。アルファベットは26文字のため、ROT -13はROT 13と一致し、そのためROT13でエンコードしたものはROT13でデコードすることができます。このエンコード・デコードの向きを気にしなくていい対象性も、上記のユースケースでROT13が好まれた理由の一つだと考えています。例えば「ROT 5です」と言われて暗号文を渡されたときに、+5したらデコードできるのか-5したらデコードできるのか迷うことがあるので。

        古くは古代ローマのカエサル(シーザー)がこの方式の暗号を用いたという逸話から、カエサル暗号・シーザー暗号という呼び名もあります。当時でもこの方式に暗号としての十分な強度があったとは考えづらく、もう少し複雑な文脈があるか、あるいは根も葉もないか・・と個人的には考えていますが、調査するのも難しいため踏み込みません。

        ROTという呼び名はアルファベットの環を回すイメージでRotateあたりの単語由来かと思われます。
        
        """,

        'how_to_use_tool':
        """
        No contents yet.
        
        """,

        'test_cases':
        """
        No contents yet.
        
        """,

        'challenge':
        """
        No contents yet.
        
        """,
    },
}


def output_with_tag(text):
    text = text.strip()
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
        return {'title': contents[pageid]['title'],
                'about': output_with_tag(contents[pageid]['about']),
                'how_to_use_tool': output_with_tag(contents[pageid]['how_to_use_tool']),
                'test_cases': output_with_tag(contents[pageid]['test_cases']),
                'challenge': output_with_tag(contents[pageid]['challenge']), }
