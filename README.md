# coverpy
Automatically write cover letters from templates via args or stdin 

# Usage:

### If you don't know the args of the template you are using

./coverpy.py -file <templatefile>  -  output is saved to <templatefile>_out.txt
./coverpy.py -file <templatefile>  -outfile <output_file>  -  output is saved to <outputfile>
  
### If you do know the args of the template you are using (example using basictemplate.txt)

./coverpy.py -file basictemplate.txt -tname Bob -position hackerman -source LinkedIn -study_year 4th -course "Ethical Hacking" -university Abertay -yname -outfile test.txt

Any args you don't specify will be requested through stdin (notice yname).
