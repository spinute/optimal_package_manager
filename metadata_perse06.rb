<<INTRO
仮想パッケージの除去，or_dependencyの処理を行った結果，依存対象が空の依存関係行が
存在しているのでそれを取り除く。
INTRO

dest = open('dest06.txt', 'w')

open('dest04.txt') do |file|
	begin 
		while line = file.readline
			dest.write(line) unless line.chomp.strip.end_with? ':'
		end
	rescue EOFError
	end
end
