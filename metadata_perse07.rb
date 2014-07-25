<<INTRO
:i386 の消去
INTRO

dest = open('dest07.txt', 'w')

open('dest06.txt') do |file|
	begin 
		while line = file.readline
			line.gsub!(/:i386/,'')
			dest.write(line) 
		end
	rescue EOFError
	end
end
