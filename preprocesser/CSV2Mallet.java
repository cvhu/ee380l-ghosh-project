import java.io.*;
import java.util.*;

public class CSV2Mallet{
	public File file = null;
	protected BufferedReader reader = null;
	int doc_id = 0;
	
	public CSV2Mallet(File file){
		this.file = file;
		try{
			this.reader = new BufferedReader(new FileReader(file));
		}catch(IOException e){
			System.err.println("Error reading file: "+e);
		}
	}
	
	protected String getNextLine(){
		String line = null;
		try{
			do{
				line = reader.readLine();
				if(line == null){
					reader.close();
					return null;
				}
			}while(line.equals(""));
		}catch(Exception e){
			System.err.println("error reading line: "+e);
		}
		return line;
	}
	
	protected void parseLines(){
		String line = null;
		while((line=getNextLine()) != null){
			System.out.printf("doc_%d\tX\t%s\n", doc_id, line);
			doc_id++;
		}
	}
	
	public static void main(String[] args) throws IOException{
		File csv = new File(args[0]);
		CSV2Mallet c2m = new CSV2Mallet(csv);
		c2m.parseLines();
	}
}