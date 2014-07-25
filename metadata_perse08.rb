<<INTRO
仮想パッケージを消して現れた空の依存関係の除去
INTRO

dest = open('dest08.txt', 'w')

open('dest06.txt') do |file|
	begin 
		while line = file.readline
			line.gsub!(/, +,/, ',')
			line.gsub!(/: +,/, ':')
			line.gsub!(/, +\n/, "\n")
			dest.write(line)
		end
	rescue EOFError
	end
end
