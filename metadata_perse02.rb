<<INTRO
このプログラムはmetadataをパースするためのものです。
virtual packageの
constraint: <pkg>
    pkg1
    pkg2
    .
    .
    .
    pkgn
を
constraint: <pkg>,    pkg1,    ...,    pkgn
に置き換えてくれます。
デリミタは,です。
仮想パッケージはパッケージ名でないので除きます。

引き続きmetadata_perse03.rbを通す予定です。
INTRO


dest = open('dest02.txt', 'w')

open('dest.txt') do |file|
	prev_line = file.readline
	begin
		while line = file.readline
			begin
				while line.start_with? '    '
					prev_line.sub(/\<.+\>/,'') if prev_line.match(/\<.+\>/)
					prev_line = prev_line.chomp + ',' + line
					line = file.readline
				end
			rescue EOFError 
			end
			dest.write(prev_line)
			prev_line = line
		end
	rescue 
	end
	dest.write(line)
end