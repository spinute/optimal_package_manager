<<INTRO
仮想パッケージのうち実態の無いものを除きます。
INTRO

dest = open('dest04.txt', 'w')

open('dest03.txt') do |file|
	begin
		while line = file.readline
			line.sub!(/\<.*\>/,'')
			line.sub!(/\:\s*\,/, ':')
			dest.write(line)
		end
	rescue EOFError
	end
end