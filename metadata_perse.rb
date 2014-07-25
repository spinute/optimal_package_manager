<<INTRO
このプログラムはmetadataのconstraintタグの日本語を英語で置き換えてくれます。
ubuntuの設定が日本語だったのでこんなものが必要になりました。
debianで吸い上げた方のmetadataは英語だったのでを通す必要はありません。
続いてmetadata_perse02.rbを通す予定です。
INTRO

dest = open('dest.txt','w')

open('dependency.txt') do |file|
	while line=file.gets
		line.gsub!(/先行依存/,'Pre_Depends')
		line.gsub!(/依存/,'Depends')
		line.gsub!(/提案/,'Suggests')
		line.gsub!(/競合/,'Conflicts')
		line.gsub!(/破壊/,'Breaks')
		line.gsub!(/推奨/,'Reccomends')
		line.gsub!(/置換/,'Replaces')
		line.gsub!(/拡張/,'Enhances')
		
		dest.write(line)
	end
end