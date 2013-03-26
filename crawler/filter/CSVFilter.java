import java.io.*;
import java.util.*;

public class CSVFilter{
	public static void buildOut(String pid){	
		try{
			File o = new File("out/"+pid+".txt");
			OutputStream out = new FileOutputStream(o);
			File a = new File("src/"+pid+"_abstract.txt");
			BufferedReader reader = new BufferedReader(new FileReader(a));		
			String line = reader.readLine();
			while(line!=null){
				out.write(line.getBytes());
				line = reader.readLine();
			}

			File c = new File("src/"+pid+"_claims.txt");
			reader = new BufferedReader(new FileReader(c));		
			line = reader.readLine();
			while(line!=null){
				out.write(line.getBytes());
				line = reader.readLine();
			}			
		}catch(Exception e){
			System.err.println(e);
		}
	}
	
	public static void main(String[] args) throws IOException{
		try{
			File input = new File(args[0]);
			BufferedReader reader = new BufferedReader(new FileReader(input));
			String line = reader.readLine();
			while(line != null){	
				System.out.println(line);
				buildOut(line);		
				line = reader.readLine();				
			}			
		}catch(Exception e){
			System.err.println(e);
		}
	}	
}