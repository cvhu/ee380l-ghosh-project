import org.jsoup.nodes.*;
import org.jsoup.select.*;
import org.jsoup.*;

import java.io.*;
import java.util.*;

public class MCrawlerUrl{
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
		String dir = "maureen_app/";
		StringBuffer sb = new StringBuffer();
		
		File pats = new File(dir+"patents.csv");
		OutputStream pats_out = new FileOutputStream(pats);
		String pats_header = "pat_id, title, USP#, date, assignee, city, state, family_id, filed_date, us_class, int_class, cpc_class, url\n";
		pats_out.write(pats_header.getBytes());
		
		File auths = new File(dir+"authorships.csv");
		OutputStream auths_out = new FileOutputStream(auths);
		String auths_header = "pat_id, a_id\n";
		auths_out.write(auths_header.getBytes());
		
		File mFile = new File("Maureen_url.csv");
		BufferedReader mReader = new BufferedReader(new FileReader(mFile));
		String mLine = mReader.readLine();
		
		File file;
		OutputStream out;
		String p_id, pURL;
		int i = 0;
		while(mLine != null && mLine.length() != 0){
			pURL = mLine;			
			p_id = "pat"+(i+1);
			mLine = mReader.readLine();
			i++;
			// System.out.println(sb.toString());
			try{
				Connection connection = Jsoup.connect(pURL);
				connection.timeout(20000);
				Document doc = connection.get();
			
			
				System.out.printf("writing %s meta data...\n", p_id);
				try{
					sb = new StringBuffer();
					sb.append(p_id+", ");
					// Title
					sb.append(doc.select("font[size=+1]").get(0).text().replace(",", " ")+", ");
					// System.out.println("... so far "+sb.toString());
					Element table1 = doc.select("table[width=100%]").get(1);
					// System.out.println(table1.html());
					// USP#
								sb.append(table1.getElementsByTag("tr").get(0).getElementsByTag("td").get(1).text().replace(",", "")+", ");
					// System.out.println("... so far "+sb.toString());
					// date
					sb.append(table1.getElementsByTag("tr").last().getElementsByTag("td").get(1).text().replace(",", " ")+", ");
				
					// System.out.println("... so far "+sb.toString());
				
					String corp = "";
					try{
						String assignee = doc.getElementsContainingOwnText("Assignee:").get(0).nextElementSibling().text();
						int aci = assignee.indexOf("(");
						String company = assignee;
						String city = "";
						String state = "";
						if(aci>=0){
							company = assignee.substring(0,aci).replace(",", " ").toLowerCase();
							String cityState = assignee.substring(aci+1, assignee.indexOf(")"));
							city = cityState.substring(0,cityState.indexOf(",")).replace(",", " ").toLowerCase();
							state = cityState.substring(cityState.indexOf(",")+1).replace(",", " ").toLowerCase();
						}						
						corp = company+", "+city+", "+state;
						sb.append(corp+",");
					}catch(Exception e){
						sb.append(", , ,");
						System.err.println("Asignee doesn't exist: "+e);
					}
					// System.out.println("Corp: "+corp);
				
				
				
					sb.append(doc.getElementsContainingOwnText("Family ID:").get(0).nextElementSibling().text().replace(",", " ")+", ");
				
					// sb.append(doc.getElementsContainingOwnText("Appl. No.:").get(0).nextElementSibling().text().replace(",", "")+", ");
				
					sb.append(doc.getElementsContainingOwnText("Filed:").get(0).nextElementSibling().text().replace(",", " ")+", ");
				
					sb.append(doc.getElementsContainingOwnText("U.S. Class:").get(0).parent().nextElementSibling().text().replace(",", " ")+", ");
				
					sb.append(doc.getElementsContainingOwnText("International Class:").get(0).parent().nextElementSibling().text().replace(",", " ")+", ");
				
					sb.append(doc.getElementsContainingOwnText("CPC Class:").get(0).parent().nextElementSibling().text().replace(",", " ")+","+pURL+"\n");
				
					// System.out.println("... so far "+sb.toString());
					
					pats_out.write(sb.toString().getBytes());

					try{
						StringBuffer sba;
						String inventors = doc.getElementsContainingOwnText("Inventors:").get(0).nextElementSibling().text();										
						int del = inventors.indexOf(")");
						String inventor;
						while(del != -1){
							sba = new StringBuffer();
							inventor = inventors.substring(0,del);
							sba.append(inventor.substring(0, inventor.indexOf("(")-1).trim()+",");
							sba.append(inventor.substring(inventor.indexOf("(")+1, inventor.indexOf(",")).trim()+",");
							sba.append(inventor.substring(inventor.indexOf(",")+1).trim()+",");						
							sba.append(corp);
							String applicant = sba.toString();
							String a_id = searchApplicant(applicant.toLowerCase());						
							String authorship = p_id+", "+a_id + "\n";
							auths_out.write(authorship.getBytes());
							if(inventors.length() < del+3){
								break;
							}
							inventors = inventors.substring(del+3);						
							del = inventors.indexOf(")");				
							// System.out.println(sba.toString());
						}					
					}catch(Exception e2){
						System.err.println("Inventors cannot be found: "+e2);
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
					String text = doc.text();
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
			}catch(Exception e){
				System.err.printf("Invalid URL: %s\n", pURL);
			}
		}	
		pats_out.close();
		auths_out.close();	
		
		File apps = new File(dir+"applicants.csv");
		OutputStream apps_out = new FileOutputStream(apps);
		String apps_header = "a_id, name, city, state, company, company city, company state\n";
		apps_out.write(apps_header.getBytes());
		for(String applicant : applicantsMap.keySet()){
			String entry = applicantsMap.get(applicant) + ", " + applicant +"\n";
			apps_out.write(entry.getBytes());
		}
		apps_out.close();
		
	}
}