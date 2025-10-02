// MAX AI Research Assistant - Neo4j Knowledge Graph Schema
// Citation Network Analysis, Research Communities, Knowledge Discovery
// Version: 1.0.0

// ============================================================================
// CONSTRAINTS & INDEXES
// ============================================================================

// Paper nodes
CREATE CONSTRAINT paper_id_unique IF NOT EXISTS FOR (p:Paper) REQUIRE p.paper_id IS UNIQUE;
CREATE CONSTRAINT paper_external_id_unique IF NOT EXISTS FOR (p:Paper) REQUIRE p.external_id IS UNIQUE;
CREATE INDEX paper_title_index IF NOT EXISTS FOR (p:Paper) ON (p.title);
CREATE INDEX paper_year_index IF NOT EXISTS FOR (p:Paper) ON (p.publication_year);
CREATE INDEX paper_citations_index IF NOT EXISTS FOR (p:Paper) ON (p.citations_count);

// Author nodes
CREATE CONSTRAINT author_id_unique IF NOT EXISTS FOR (a:Author) REQUIRE a.author_id IS UNIQUE;
CREATE INDEX author_name_index IF NOT EXISTS FOR (a:Author) ON (a.name);
CREATE INDEX author_hindex_index IF NOT EXISTS FOR (a:Author) ON (a.h_index);

// Venue nodes
CREATE CONSTRAINT venue_name_unique IF NOT EXISTS FOR (v:Venue) REQUIRE v.name IS UNIQUE;
CREATE INDEX venue_type_index IF NOT EXISTS FOR (v:Venue) ON (v.venue_type);

// Topic/Field nodes
CREATE CONSTRAINT topic_name_unique IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE;

// Institution nodes
CREATE CONSTRAINT institution_name_unique IF NOT EXISTS FOR (i:Institution) REQUIRE i.name IS UNIQUE;

// Research Community nodes
CREATE CONSTRAINT community_id_unique IF NOT EXISTS FOR (c:Community) REQUIRE c.community_id IS UNIQUE;

// ============================================================================
// NODE LABELS & PROPERTIES
// ============================================================================

// Paper node properties
// (:Paper {
//     paper_id: UUID,
//     external_id: String,
//     title: String,
//     abstract: String,
//     publication_year: Integer,
//     publication_date: Date,
//     doi: String,
//     arxiv_id: String,
//     citations_count: Integer,
//     references_count: Integer,
//     influential_citation_count: Integer,
//     credibility_score: Float,
//     h_index: Integer,
//     tldr: String,
//     is_open_access: Boolean,
//     embedding: List<Float>, // 768-dim vector
//     keywords: List<String>,
//     created_at: DateTime,
//     pagerank_score: Float,
//     betweenness_centrality: Float,
//     closeness_centrality: Float
// })

// Author node properties
// (:Author {
//     author_id: UUID,
//     name: String,
//     normalized_name: String,
//     orcid: String,
//     google_scholar_id: String,
//     h_index: Integer,
//     i10_index: Integer,
//     total_citations: Integer,
//     total_papers: Integer,
//     research_interests: List<String>,
//     homepage_url: String,
//     created_at: DateTime,
//     pagerank_score: Float
// })

// Venue node properties
// (:Venue {
//     venue_id: UUID,
//     name: String,
//     venue_type: String, // journal, conference, workshop
//     issn: String,
//     impact_factor: Float,
//     h_index: Integer,
//     publisher: String
// })

// Topic/Field node properties
// (:Topic {
//     topic_id: UUID,
//     name: String,
//     parent_topic: String,
//     level: Integer, // hierarchy level
//     paper_count: Integer,
//     total_citations: Integer
// })

// Institution node properties
// (:Institution {
//     institution_id: UUID,
//     name: String,
//     country: String,
//     city: String,
//     website: String,
//     type: String // university, research_institute, company
// })

// Research Community node properties
// (:Community {
//     community_id: UUID,
//     name: String,
//     detection_algorithm: String, // louvain, label_propagation, etc.
//     member_count: Integer,
//     paper_count: Integer,
//     modularity_score: Float,
//     created_at: DateTime
// })

// ============================================================================
// RELATIONSHIP TYPES
// ============================================================================

// Paper -> Paper relationships
// [:CITES] - One paper cites another
// Properties: context, intent, is_influential, created_at

// [:REFERENCES] - Inverse of CITES

// [:SIMILAR_TO] - Papers with similar content/embedding
// Properties: similarity_score, method

// [:CO_CITED_WITH] - Papers cited together frequently
// Properties: co_citation_count, strength

// [:BIBLIOGRAPHIC_COUPLING] - Papers that cite the same references
// Properties: coupling_strength, shared_references_count

// Paper -> Author relationships
// [:AUTHORED_BY] - Paper written by author
// Properties: author_position, is_corresponding, affiliation_at_time

// [:FIRST_AUTHORED_BY] - Specifically first author

// Paper -> Venue relationships
// [:PUBLISHED_IN] - Paper published in venue
// Properties: volume, issue, pages, publication_date

// Paper -> Topic relationships
// [:ABOUT] - Paper is about topic
// Properties: relevance_score, confidence

// Author -> Author relationships
// [:COLLABORATED_WITH] - Authors who co-authored papers
// Properties: collaboration_count, paper_ids, first_collaboration, last_collaboration

// [:MENTORED] - Advisor-mentee relationship
// Properties: start_year, end_year, institution

// [:SAME_INSTITUTION] - Authors at same institution
// Properties: institution_name, period

// Author -> Institution relationships
// [:AFFILIATED_WITH] - Author works at institution
// Properties: start_date, end_date, role, is_current

// Community relationships
// [:BELONGS_TO] - Paper/Author belongs to community
// Properties: membership_strength, assigned_at

// [:BRIDGES_TO] - Community has connections to another
// Properties: edge_count, betweenness

// Topic relationships
// [:SUBTOPIC_OF] - Topic hierarchy
// Properties: level

// [:RELATED_TO] - Topics frequently co-occurring
// Properties: co_occurrence_count, pmi_score

// ============================================================================
// SAMPLE QUERIES & ALGORITHMS
// ============================================================================

// Find influential papers (high PageRank)
// MATCH (p:Paper)
// WHERE p.pagerank_score > 0.001
// RETURN p.title, p.pagerank_score, p.citations_count
// ORDER BY p.pagerank_score DESC
// LIMIT 20;

// Find research communities (Louvain algorithm)
// CALL gds.louvain.stream('citation-network')
// YIELD nodeId, communityId
// RETURN gds.util.asNode(nodeId).title AS paper, communityId
// ORDER BY communityId;

// Find shortest path between two papers
// MATCH path = shortestPath(
//   (p1:Paper {paper_id: $paper1_id})-[:CITES*]-(p2:Paper {paper_id: $paper2_id})
// )
// RETURN path;

// Find co-citation clusters
// MATCH (p1:Paper)-[:CITES]->(cited:Paper)<-[:CITES]-(p2:Paper)
// WHERE p1 <> p2
// RETURN p1.title, p2.title, COUNT(cited) as co_citations
// ORDER BY co_citations DESC
// LIMIT 50;

// Find prolific collaborators
// MATCH (a1:Author)-[c:COLLABORATED_WITH]->(a2:Author)
// WHERE c.collaboration_count > 5
// RETURN a1.name, a2.name, c.collaboration_count
// ORDER BY c.collaboration_count DESC;

// Find emerging topics (recent papers with high growth)
// MATCH (p:Paper)-[:ABOUT]->(t:Topic)
// WHERE p.publication_year >= date().year - 2
// WITH t, COUNT(p) as recent_papers
// WHERE recent_papers > 10
// RETURN t.name, recent_papers
// ORDER BY recent_papers DESC;

// Find paper influence cascade
// MATCH path = (start:Paper)-[:CITES*1..3]->(cited:Paper)
// WHERE start.paper_id = $paper_id
// RETURN path;

// Find authors with most cross-disciplinary work
// MATCH (a:Author)-[:AUTHORED_BY]-(p:Paper)-[:ABOUT]->(t:Topic)
// WITH a, COUNT(DISTINCT t) as topic_diversity
// WHERE topic_diversity > 5
// RETURN a.name, topic_diversity
// ORDER BY topic_diversity DESC;

// ============================================================================
// GRAPH DATA SCIENCE ALGORITHMS
// ============================================================================

// Create projection for citation network analysis
// CALL gds.graph.project(
//     'citation-network',
//     ['Paper', 'Author'],
//     {
//         CITES: {orientation: 'NATURAL'},
//         AUTHORED_BY: {orientation: 'UNDIRECTED'},
//         COLLABORATED_WITH: {orientation: 'UNDIRECTED'}
//     },
//     {
//         nodeProperties: ['citations_count', 'h_index', 'publication_year'],
//         relationshipProperties: ['is_influential', 'collaboration_count']
//     }
// );

// PageRank for paper importance
// CALL gds.pageRank.write('citation-network', {
//     writeProperty: 'pagerank_score',
//     dampingFactor: 0.85,
//     maxIterations: 20
// });

// Betweenness Centrality for finding bridge papers
// CALL gds.betweenness.write('citation-network', {
//     writeProperty: 'betweenness_centrality'
// });

// Community Detection (Louvain)
// CALL gds.louvain.write('citation-network', {
//     writeProperty: 'community_id',
//     includeIntermediateCommunities: true
// });

// Node Similarity for paper recommendations
// CALL gds.nodeSimilarity.write('citation-network', {
//     writeRelationshipType: 'SIMILAR_TO',
//     writeProperty: 'similarity_score',
//     similarityCutoff: 0.5
// });

// Label Propagation for quick community detection
// CALL gds.labelPropagation.write('citation-network', {
//     writeProperty: 'community_label',
//     maxIterations: 10
// });

// ============================================================================
// MAINTENANCE QUERIES
// ============================================================================

// Update citation counts
// MATCH (p:Paper)<-[c:CITES]-()
// WITH p, count(c) as citation_count
// SET p.citations_count = citation_count;

// Update collaboration counts
// MATCH (a1:Author)-[:AUTHORED_BY]-(p:Paper)-[:AUTHORED_BY]-(a2:Author)
// WHERE id(a1) < id(a2)
// WITH a1, a2, count(DISTINCT p) as collab_count
// MERGE (a1)-[c:COLLABORATED_WITH]->(a2)
// SET c.collaboration_count = collab_count;

// Clean up orphaned nodes
// MATCH (p:Paper)
// WHERE NOT (p)-[:CITES|CITES_BY|AUTHORED_BY]-()
// DELETE p;

// ============================================================================
// EXAMPLE DATA LOADING
// ============================================================================

// Load papers from CSV
// LOAD CSV WITH HEADERS FROM 'file:///papers.csv' AS row
// CREATE (p:Paper {
//     paper_id: row.paper_id,
//     external_id: row.external_id,
//     title: row.title,
//     publication_year: toInteger(row.publication_year),
//     citations_count: toInteger(row.citations_count)
// });

// Create citation relationships from CSV
// LOAD CSV WITH HEADERS FROM 'file:///citations.csv' AS row
// MATCH (citing:Paper {paper_id: row.citing_id})
// MATCH (cited:Paper {paper_id: row.cited_id})
// CREATE (citing)-[:CITES {
//     is_influential: toBoolean(row.is_influential),
//     created_at: datetime()
// }]->(cited);

// ============================================================================
// PERFORMANCE TIPS
// ============================================================================

// 1. Always use MERGE instead of CREATE for entities that might already exist
// 2. Create indexes on frequently queried properties
// 3. Use parameters for query values to enable query caching
// 4. Limit result sets with LIMIT clause
// 5. Use PROFILE/EXPLAIN to analyze query performance
// 6. Consider using APOC procedures for complex operations
// 7. Batch large imports using periodic commits
// 8. Run graph algorithms on projected graphs (GDS)
// 9. Regularly run CALL db.stats() to monitor graph size
// 10. Use relationship properties judiciously (can impact traversal speed)

RETURN 'MAX Neo4j Knowledge Graph Schema initialized successfully' AS status;
