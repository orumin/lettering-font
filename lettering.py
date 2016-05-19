#!/usr/bin/env fontforge -lang=py -script
# -*- coding: utf-8 -*-

import fontforge
from datetime import date

# SpecialElite のあるディレクトリのパス
special_elite_path = "./special_elite"

# Oradano明朝 のあるディレクトリのパス
oradano_mincho_path = "./oradano_mincho/Oradano2016-0427t"

# Lettering を生成するディレクトリのパス
# 同じディレクトリに一時ファイルも生成される
lettering_path = "./"

# フォントリスト
# SpecialElite ファイル名, Oradano明朝 ファイル名, Lettering ウェイト
font_list = [
    ("SpecialElite.ttf", "Oradano-mincho-t.ttf", "Regular"),
]

def main():
    # 縦書き対応
    fontforge.setPrefs('CoverageFormatsAllowed', 1)

    # バージョンを今日の日付から生成する
    today = date.today()
    version = "Lettering-{0}".format(today.strftime("%Y%m%d"))

    for (se, om, weight) in font_list:
        se_path = "{0}/{1}".format(special_elite_path, se)
        om_path = "{0}/{1}".format(oradano_mincho_path, om)
        le_path = "{0}/Lettering-{1}.ttf".format(lettering_path, weight)
        generate_lettering(se_path, om_path, le_path, weight, version)

def lettering_sfnt_names(weight, version):
    return (
        ('English (US)', 'Copyright',
         '''\
         Lettering: Copylight (c) 2016 orumin.

         Special Elite: Copyright (c) 2011 Google Corporation.

	 Oradano Mincho: Copyright (C) 2016 UCHIDA Akira.'''),
        ('English (US)', 'Family', 'Lettering {0}'.format(weight)),
        ('English (US)', 'SubFamily', weight),
        ('English (US)', 'Fullname', 'Lettering-{0}'.format(weight)),
        ('English (US)', 'Version', version),
        ('English (US)', 'PostScriptName', 'Lettering-{0}'.format(weight)),
        ('English (US)', 'Vendor URL', 'http://orum.in'),
        ('English (US)', 'Preferred Family', 'Lettering'),
        ('English (US)', 'Preferred Styles', weight),
        ('Japanese', 'Preferred Family', 'Lettering'),
        ('Japanese', 'Preferred Styles', weight),
    )

def lettering_gasp():
    return (
        (8, ('antialias',)),
        (13, ('antialias', 'symmetric-smoothing')),
        (65535, ('gridfit', 'antialias', 'symmetric-smoothing', 'gridfit+smoothing')),
    )

def generate_lettering(se_path, om_path, le_path, weight, version):
    # Oradana明朝 を開く
    font = fontforge.open(om_path)

    # EMの大きさを2048に設定する
    font.em = 2048

    # SpecialElite を開く
    sefont = fontforge.open(se_path)

    # SpecialElite に含まれるグリフを削除する
    font.selection.none()
    sefont.selection.all()
    for glyph in sefont.selection.byGlyphs:
        if glyph.glyphname in font:
            font.selection.select(("more",), glyph.glyphname)
    font.clear()
        
    # SpecialElite をマージする
    font.mergeFonts(se_path)

    # フォント情報の設定
    font.sfnt_names = lettering_sfnt_names(weight, version)
    font.os2_vendor = "ltrg"

    # Grid Fittingの設定
    font.gasp = lettering_gasp()

    # TTF の生成
    font.generate(le_path, '', ('short-post', 'opentype', 'PfEd-lookups'))

if __name__ == '__main__':
    main()
