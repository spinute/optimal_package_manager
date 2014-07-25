<<INTRO
pythonが食べやすいようにconstraintのアタマに付いている|を処理して，
or constraintを一行にまとめます。
デリミタは,です。
前に出てくるpackageが後ろにくっつくのは仕様です。
（後ろからdependency.txtを回せば解決すると思うけど今は問題ないしめんどくさかった）
INTRO

dest = open('dest03.txt', 'w')

open('dest02.txt') do |file|
	line = file.readline
	begin
		while next_line = file.readline
			if line.start_with?(' |')
				line = next_line.chomp + line.sub(/^ \|\w*:/,' , ') 
			else
				dest.write(line)
				line = next_line
			end
		end
	rescue EOFError
	end
	dest.write(next_line)
end