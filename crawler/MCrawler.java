import org.jsoup.nodes.*;
import org.jsoup.select.*;
import org.jsoup.*;

import java.io.*;
import java.util.*;

//java Crawler input.csv output.csv dir

public class MCrawler{
	static int count = 0;
	static OutputStream out;
	static String dir;
	
	public static void tokenize(String line, LinkedList<String> ll){
		int i = 0;
		int f = 0;
		System.out.println("\n"+line);
		System.out.println(line.substring(1).indexOf('\"'));
		while(i < line.length()){
			char c = line.charAt(i);
			if(c=='"'){				
				f = line.substring(i+1).indexOf('\"');
				ll.add(line.substring(i+1, f));
				i = f + 1;
			}else if(c==','){
				f = line.substring(i+1).indexOf(',');
				ll.add(line.substring(i+1, f));
				i = f + 1;
			}else{
				i++;
			}			
		}
		System.out.println(ll.toString());
	}
	public static void crawl(String line){
		// StringTokenizer st = new StringTokenizer(line, ",");		
		// System.out.println("tokenized "+st.countTokens());
		String pid = "pat"+count;
		count++;
		LinkedList<String> ll = new LinkedList<String>();
		tokenize(line, ll);
		// String pn = st.nextToken();
		// String ta = st.nextToken();
		// String city = st.nextToken();
		// String state = st.nextToken();
		// String country = st.nextToken();
		// String url = st.nextToken();
		// String status;
		// String cpc_class;	
		// System.out.println("tokenization finished");	
		// try{
		// 	Connection connection = Jsoup.connect(url);
		// 	connection.timeout(20000);
		// 	System.out.println("connected");
		// 	Document doc = connection.get();
		// 	status = "valid";
		// 	cpc_class = doc.getElementsContainingOwnText("CPC Class:").get(0).parent().nextElementSibling().text().replace(",", " ");			
		// 	System.out.println("crawled cpc");
		// 	File file;
		// 	FileOutputStream fo;
		// 	System.out.printf("writing %s ...\n", pid);
		// 	try{
		// 		file = new File(dir+"/"+pid+".txt");
		// 		fo = new FileOutputStream(file);
		// 		String t = doc.select("center>b").get(0).parent().nextElementSibling().text();
		// 		String text = doc.text();
		// 		int ci = text.indexOf("Claims");
		// 		int di = text.indexOf("Description");
		// 	 	t = t+"\n"+text.substring(ci, di);
		// 		fo.write(t.getBytes());
		// 		fo.close();				
		// 	}catch(Exception e){
		// 		System.err.println("Cannot find abstract: "+e);
		// 	}		
		// }catch(Exception e){
		// 	status = "invalid";
		// 	cpc_class="";
		// 	System.err.println("invalid url"+e);
		// }
		// 
		// try{
		// 	String outLine = pid+","+pn+","+ta+","+city+","+state+","+country+","+url+","+status+","+cpc_class+"\n";
		// 	out.write(outLine.getBytes());
		// }catch(Exception e){
		// 	System.err.println("cannot write output"+e);
		// }
	}
	
	
	public static void main(String[] args) throws IOException{
		try{			
			File input = new File(args[0]);
			System.out.println("read input");
			File output = new File(args[1]);
			System.out.println("read output");
			dir = args[2];
			System.out.println("read dir");
			OutputStream out = new FileOutputStream(output);
			System.out.println("create out stream");
			String header = "pid, patent #, tech area, city, state, country, url, status, cpc_class\n";
			out.write(header.getBytes());
			System.out.println("read header");
			BufferedReader reader = new BufferedReader(new FileReader(input));
			System.out.println("read input line");
			String line = reader.readLine();
			while(line != null){
				System.out.println("crawl "+line);
				crawl(line);
				line = reader.readLine();
			}
		}catch(Exception e){
			System.err.println("invalid input command "+e);
		}
	}
}