from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.document_parser import parse_document
from services.clause_splitter import split_into_clauses
from services.analyzer import analyze_clause

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):

    text = parse_document(file.file, file.filename)
    clauses = split_into_clauses(text)

    results = []

    for clause in clauses[:5]:  # limit for MVP
        result = analyze_clause(clause)
        results.append(result)

    # Risk scoring
    risk_map = {"Low": 1, "Medium": 2, "High": 3}
    total_score = sum(risk_map[r["risk_level"]] for r in results)
    avg_score = round(total_score / len(results), 2)

    overall_risk = (
        "Low" if avg_score <= 1.5
        else "Medium" if avg_score <= 2.3
        else "High"
    )

    return {
        "overall_risk": overall_risk,
        "risk_score": avg_score,
        "clauses_analyzed": len(results),
        "analysis": results
    }