<<INTRO
重複パッケージ名の除去
INTRO

dest = open('dest09.txt', 'w')

open('dest08.txt') do |file|
	begin 
		while line = file.readline
			buf = line.split(': ').map!{|e| e.split(',').map!(&:strip)}.flatten.uniq
			if buf.size > 1
				line = '  ' + buf[0] + ': '
				1.upto(buf.size-1) {|i| line += buf[i] + ','}
				line.chop!
				line += "\n"
			end
			dest.write(line)
		end
	rescue EOFError
	end
end
