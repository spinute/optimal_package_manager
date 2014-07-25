<<INTRO
meta_perse04の出力ファイルをさらにパース
パッケージ名にアーキテクチャ名が付いているものを除きます。
（ここでの処理が必要かどうか，あるいは処理が必要かどうかを判断するにはアーキテクチャの情報を取得必要があり，
実際には実行時にシステムコールを呼び出す必要があるかと思います。）
INTRO

dest = open('dest05.txt', 'w')

open('dest04.txt') do |file|
	begin
		while line = file.readline
			line.sub!(/:i386/,'')
			dest.write(line)
		end
	rescue EOFError
	end
end