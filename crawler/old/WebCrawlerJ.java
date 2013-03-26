import org.jsoup.nodes.*;
import org.jsoup.select.*;
import org.jsoup.*;
import org.json.*;

import java.io.*;
import java.util.*;

public class WebCrawlerJ{
	protected static HashMap<String, String> applicantsMap = new HashMap<String, String>();
	protected static int acount = 0;
	
	protected static String searchApplicant(String applicant){
		String a_id = applicantsMap.get(applicant);
		if(a_id == null){
			acount++;
			a_id = "a"+acount;
			applicantsMap.put(applicant, a_id);
		}
		return a_id;
	}
	
	public static void main(String[] args) throws IOException{
		int n = 4719;
		String dir = "mounting_photovoltaic/";
		StringBuffer sb = new StringBuffer();
		String front = "http://appft1.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=";
		String back = "&f=G&l=50&co1=AND&d=PG01&s1=mounting&s2=photovoltaic&OS=&RS=";
		
		File pats = new File(dir+"patents.csv");
		OutputStream pats_out = new FileOutputStream(pats);
		String pats_header = "pat_id, title, USPA#, kind_code, date, serial#, series_code, field_date, us_class, pub_class, int_class, assignee, city, state\n";
		pats_out.write(pats_header.getBytes());
		
		File auths = new File(dir+"authorships.csv");
		OutputStream auths_out = new FileOutputStream(auths);
		String auths_header = "pat_id, a_id\n";
		auths_out.write(auths_header.getBytes());
		
		File file;
		OutputStream out;
		String p_id;
		for(int i = 0; i < n; i++){
			p_id = "pat"+(i+1);
			sb = new StringBuffer();
			sb.append(front);
			sb.append(i+1);
			sb.append(back);
			Connection connection = Jsoup.connect(sb.toString());
			connection.timeout(20000);
			Document doc = connection.get();
			
			
			System.out.printf("writing %s meta data...\n", p_id);
			try{
				sb = new StringBuffer();
				sb.append(p_id+", ");
				sb.append(doc.select("font[size=+1]").get(0).text().replace(",", " ")+", ");
				
				Element table1 = doc.getElementsContainingOwnText("Kind Code").get(0).parent().parent().parent();
				sb.append(table1.getElementsByTag("tr").get(0).getElementsByTag("td").get(1).text().replace(",", " ")+", ");
				sb.append(table1.getElementsByTag("tr").get(1).getElementsByTag("td").get(1).text().replace(",", " ")+", ");
				sb.append(table1.getElementsByTag("tr").get(2).getElementsByTag("td").get(1).text().replace(",", " ")+", ");
				
				Element table2 = doc.getElementsContainingOwnText("Serial No.").get(0).parent().parent().parent();
				sb.append(table2.getElementsContainingOwnText("Serial No.:").get(0).nextElementSibling().text().replace(",", " ")+", ");
				sb.append(table2.getElementsContainingOwnText("Series Code:").get(0).nextElementSibling().text().replace(",", " ")+", ");
				sb.append(table2.getElementsContainingOwnText("Filed:").get(0).nextElementSibling().text().replace(",", " ")+", ");
				
				Element table3 = doc.getElementsContainingOwnText("Class at Publication:").get(0).parent().parent().parent();
				sb.append(table3.getElementsByTag("tr").get(0).getElementsByTag("td").get(1).text().replace(",", " ")+", ");
				sb.append(table3.getElementsByTag("tr").get(1).getElementsByTag("td").get(1).text().replace(",", " ")+", ");
				sb.append(table3.getElementsByTag("tr").get(2).getElementsByTag("td").get(1).text().replace(",", " "));
				String corp = "";
				try{
					Element assignee = doc.select("table[width=100%]").get(2).getElementsContainingOwnText("Assignee:").get(0).nextElementSibling();
					String company = assignee.getElementsByTag("b").get(0).text().replace(",", " ").toLowerCase();
					String city = assignee.getElementsByTag("b").get(1).text().replace(",", " ").toLowerCase();
					String state = assignee.getElementsByTag("b").get(2).text().replace(",", " ").toLowerCase();
					corp = company+", "+city+", "+state;
					sb.append(", "+corp+"\n");
				}catch(Exception e){
					sb.append(", , , \n");
					System.err.println("Asignee doesn't exist: "+e);
				}
				
				pats_out.write(sb.toString().getBytes());
				
				try{
					StringBuffer sba = new StringBuffer();
					Element applicants_table = doc.getElementsContainingOwnText("Applicant:").get(0).nextElementSibling();
					Element names = applicants_table.getElementsByTag("tr").get(1).child(0).child(0);
					Scanner namesS = new Scanner(names.html()).useDelimiter("<br />");
					Element cities = applicants_table.getElementsByTag("tr").get(1).child(1);					
					Scanner citiesS = new Scanner(cities.html()).useDelimiter("<br />");
					Element states = applicants_table.getElementsByTag("tr").get(1).child(2);
					Scanner statesS = new Scanner(states.html()).useDelimiter("<br />");
					Element countries = applicants_table.getElementsByTag("tr").get(1).child(3);
					Scanner countriesS = new Scanner(countries.html()).useDelimiter("<br />");
					while(namesS.hasNext()){
						sba = new StringBuffer();
						sba.append(namesS.next().replace(",", " ")+", ");
						if(citiesS.hasNext()){
							sba.append(citiesS.next().replace(",", " ")+", ");
						}else{
							sba.append(", ");
						}
						if(statesS.hasNext()){
							sba.append(statesS.next().replace(",", " ")+", ");
						}else{
							sba.append(", ");
						}
						if(countriesS.hasNext()){
							sba.append(countriesS.next().replace(",", " ")+", ");
						}else{
							sba.append(", ");
						}
						sba.append(corp);
						String applicant = sba.toString();
						String a_id = searchApplicant(applicant.toLowerCase());						
						String authorship = p_id+", "+a_id + "\n";
						auths_out.write(authorship.getBytes());
					}
				}catch(Exception e){
					System.err.println("Applicants cannot be found: "+e);
					try{
						StringBuffer sba = new StringBuffer();
						Elements inventors = table2.getElementsContainingOwnText("Inventors:").get(0).nextElementSibling().select("b");
						for(int k = 0; k < inventors.size(); k++){
							sba = new StringBuffer();
							sba.append(inventors.get(k).text().replace(",", " ")+" ,");
							String location = inventors.get(k).nextElementSibling().text().replace("(","").replace(")","");
							StringTokenizer locationST = new StringTokenizer(location, ",");
							String city = "";
							if(locationST.hasMoreTokens()){
								city = locationST.nextToken().toLowerCase().replace(",", " ");
							}
							String state = "";
							if(locationST.hasMoreTokens()){
								state = locationST.nextToken().toLowerCase().replace(",", " ");
							}
							sba.append(city+",");
							sba.append(state+",,");
							sba.append(corp);
							String applicant = sba.toString();
							String a_id = searchApplicant(applicant.toLowerCase());						
							String authorship = p_id+", "+a_id + "\n";
							auths_out.write(authorship.getBytes());
						}						
					}catch(Exception e2){
						System.err.println("Inventors cannot be found: "+e2);
					}					
				}
								
			}catch(Exception e){
				System.err.println("Cannot find metadata: "+e);
			}
			
			System.out.printf("writing %s abstract...\n", p_id);
			try{
				file = new File(dir+p_id+"_abstract.txt");
				out = new FileOutputStream(file);
				String ab = doc.select("center>b").get(0).parent().nextElementSibling().text();
				out.write(ab.getBytes());
				out.close();				
			}catch(Exception e){
				System.err.println("Cannot find abstract: "+e);
			}
			
			System.out.printf("writing %s content...\n", p_id);
			try{				
				Element content = doc.select("center>b>i").get(0).parent().parent().parent();
				String text = content.text();
				int ci = text.indexOf("Claims");
				int di = text.indexOf("Description");				
				file = new File(dir+p_id+"_claims.txt");
				out = new FileOutputStream(file);
				out.write(text.substring(ci, di).getBytes());
				out.close();				
				file = new File(dir+p_id+"_description.txt");
				out = new FileOutputStream(file);
				out.write(text.substring(di).getBytes());
				out.close();								
			}catch(Exception e){
				System.err.println("Cannot find claims: "+e);
			}
		}	
		pats_out.close();
		auths_out.close();	
		
		File apps = new File(dir+"applicants.csv");
		OutputStream apps_out = new FileOutputStream(apps);
		String apps_header = "a_id, name, city, state, country, company, company city, company state\n";
		apps_out.write(apps_header.getBytes());
		for(String applicant : applicantsMap.keySet()){
			String entry = applicantsMap.get(applicant) + ", " + applicant +"\n";
			apps_out.write(entry.getBytes());
		}
		apps_out.close();
		
	}
}