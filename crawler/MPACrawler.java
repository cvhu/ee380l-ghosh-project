import org.jsoup.nodes.*;
import org.jsoup.select.*;
import org.jsoup.*;

import java.io.*;
import java.util.*;

//java Crawler input.csv output.csv dir

public class MPACrawler{
	static int count = 0;
	static OutputStream outst;
	static String dir;
	
	public static void tokenize(String line, LinkedList<String> ll){
		int i = line.indexOf(',');	
		int j = line.indexOf('\"');
		while(i >= 0){
			// System.out.println(i);
			if(i==0){
				System.out.printf("i==0 ");
				ll.add("");				
				line = line.substring(i+1);
			}else if(j==0){
				System.out.printf("j==0 ");
				line = line.substring(1);
				j = line.indexOf('\"');
				ll.add(line.substring(0,j).replace(","," "));
				line = line.substring(j+2);
			}else{
				System.out.printf("else ");
				ll.add(line.substring(0, i));
				line = line.substring(i+1);
			}			
			i = line.indexOf(",");
			j = line.indexOf('\"');
		}
		ll.add(line);
		System.out.println(ll.size()+ll.toString());
	}
	public static void crawl(String line, OutputStream o){
		// StringTokenizer st = new StringTokenizer(line, ",");		
		// System.out.println("tokenized "+st.countTokens());
		try{
			StringBuffer sb = new StringBuffer();
			sb.append("pat");
			sb.append(count/1000);
			sb.append((count/100)%10);
			sb.append((count/10)%10);
			sb.append(count%10);
			String pid = sb.toString();
			count++;
			LinkedList<String> ll = new LinkedList<String>();
			tokenize(line.replace("(","").replace(")",""), ll);		
			String year = ll.get(0);
			String ta = ll.get(1);
			String pn = ll.get(2);
			String title = ll.get(3);
			String city = ll.get(4);
			String state = ll.get(5);
			String country = ll.get(6);
			String url = ll.get(7);
			String status = "";
			String cpc_class = "";	
			System.out.println("tokenization finished");
			try{
				Connection connection = Jsoup.connect(url);
				connection.timeout(20000);
				System.out.println("connected");
				Document doc = connection.get();
				status = "valid";
				try{
					cpc_class = doc.getElementsContainingOwnText("CPC Class:").get(0).parent().nextElementSibling().text().replace(",", " ");			
					System.out.println("crawled cpc");
				}catch(Exception e){
					status = "no CPC";
					System.err.println("CPC doesn't exist");
				}

				File file;
				FileOutputStream fo;
				System.out.printf("writing %s ...\n", pid);
				try{
					file = new File(dir+"/"+pid+".txt");
					fo = new FileOutputStream(file);
					String t = doc.select("center>b").get(0).parent().nextElementSibling().text();
					String text = doc.text();
					int ci = text.indexOf("Claims");
					int di = text.indexOf("Description");
				 	t = t+"\n"+text.substring(ci, di);
					fo.write(t.getBytes());
					fo.close();				
				}catch(Exception e){
					status = "no abstract or claims";
					System.err.println("Cannot find abstract or claims: "+e);
				}		
			}catch(Exception e){
				status = "invalid url";
				System.err.println("invalid url "+e);
			}

			try{
				String outLine = pid+","+pn+","+year+","+ta+","+title+","+city+","+state+","+country+","+url+","+status+","+cpc_class+"\n";
				// System.out.println(outLine.getBytes());
				o.write(outLine.getBytes());
			}catch(Exception e){
				System.err.println("cannot write output"+e);
			}
		}catch(Exception e){
			System.err.println("error tokenizing");
		}
	}
	
	
	public static void main(String[] args) throws IOException{
		try{			
			File input = new File(args[0]);
			System.out.println("read input");
			File output = new File(args[1]);
			System.out.println("read output");
			dir = args[2];
			System.out.println("read dir");
			OutputStream outst = new FileOutputStream(output);
			System.out.println("create out stream");
			String header = "pid, patent #, year,  tech area, title, city, state, country, url, status, cpc_class\n";
			outst.write(header.getBytes());
			System.out.println("read header");
			BufferedReader reader = new BufferedReader(new FileReader(input));
			System.out.println("read input line");
			String line = reader.readLine();
			while(line != null){
				// System.out.println("crawl "+line);
				crawl(line, outst);
				line = reader.readLine();
			}
			// BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
			// String line = stdin.readLine();
			// while(line!=null){
			// 	LinkedList<String> ll = new LinkedList<String>();
			// 	tokenize(line, ll);
			// 	line = stdin.readLine();
			// }			
		}catch(Exception e){
			System.err.println("invalid input command "+e);
		}
	}
}