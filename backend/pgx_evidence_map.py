"""
Pharmacogenomics (PGx) Evidence Map
Provides PharmGKB-style clinical evidence levels for gene-drug interactions.

Evidence Levels (modeled after PharmGKB):
  1A — Guideline-recommended (CPIC/DPWG)
  1B — Strong clinical evidence
  2A — Moderate evidence, actionable
  2B — Moderate evidence, informational
  3  — Limited evidence
  4  — Case reports only
"""

# ──────────────────────────────────────────
#  COMPREHENSIVE GENE-DRUG EVIDENCE DATABASE
# ──────────────────────────────────────────

PGX_EVIDENCE_DB = {
    # ── CYP2D6 ──
    "CYP2D6": {
        "gene_name": "Cytochrome P450 2D6",
        "chromosome": "22q13.2",
        "function": "Phase I oxidative metabolism of ~25% of clinically used drugs",
        "drugs": {
            "codeine": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "Reduced morphine formation → Decreased efficacy. Use alternative analgesic (non-tramadol opioid).",
                    "ultra_rapid_metabolizer": "Excessive morphine formation → LIFE-THREATENING respiratory depression. CONTRAINDICATED.",
                    "intermediate_metabolizer": "Reduced efficacy expected. Consider dose increase or alternative.",
                    "normal_metabolizer": "Standard response expected."
                },
                "recommendation": "Avoid codeine in CYP2D6 poor and ultra-rapid metabolizers."
            },
            "tramadol": {
                "level": "1A",
                "guideline": "CPIC/DPWG",
                "phenotype_impact": {
                    "poor_metabolizer": "Reduced O-desmethyltramadol formation → Decreased analgesic effect.",
                    "ultra_rapid_metabolizer": "Increased active metabolite → Risk of seizures and respiratory depression.",
                    "normal_metabolizer": "Standard response expected."
                },
                "recommendation": "Avoid in poor and ultra-rapid metabolizers. Use non-CYP2D6-dependent analgesic."
            },
            "fluoxetine": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "Increased plasma levels → Higher risk of side effects (nausea, agitation, QT prolongation).",
                    "ultra_rapid_metabolizer": "Sub-therapeutic levels likely → Consider alternative SSRI (sertraline, citalopram).",
                    "normal_metabolizer": "Standard response expected."
                },
                "recommendation": "Reduce dose 50% in poor metabolizers. Consider alternative in ultra-rapid."
            },
            "metoprolol": {
                "level": "1A",
                "guideline": "DPWG",
                "phenotype_impact": {
                    "poor_metabolizer": "3-5x increased exposure → Excessive bradycardia, hypotension risk.",
                    "ultra_rapid_metabolizer": "Reduced efficacy → Consider dose increase or bisoprolol.",
                    "normal_metabolizer": "Standard response expected."
                },
                "recommendation": "Reduce dose by 75% in poor metabolizers or use bisoprolol."
            },
            "tamoxifen": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "Reduced endoxifen levels → Decreased efficacy in breast cancer treatment.",
                    "ultra_rapid_metabolizer": "Enhanced activation → Standard or improved efficacy.",
                    "normal_metabolizer": "Standard response expected."
                },
                "recommendation": "Consider aromatase inhibitor instead of tamoxifen in poor metabolizers."
            },
        }
    },

    # ── CYP2C19 ──
    "CYP2C19": {
        "gene_name": "Cytochrome P450 2C19",
        "chromosome": "10q23.33",
        "function": "Metabolism of PPIs, clopidogrel, SSRIs, and benzodiazepines",
        "drugs": {
            "clopidogrel": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "CRITICAL: Reduced active metabolite → Increased thrombotic event risk (stent thrombosis, stroke).",
                    "ultra_rapid_metabolizer": "Enhanced antiplatelet effect → Slightly increased bleeding risk.",
                    "intermediate_metabolizer": "Reduced efficacy. Consider prasugrel or ticagrelor.",
                    "normal_metabolizer": "Standard response expected."
                },
                "recommendation": "Use prasugrel or ticagrelor in poor and intermediate metabolizers. FDA boxed warning."
            },
            "omeprazole": {
                "level": "1A",
                "guideline": "CPIC/DPWG",
                "phenotype_impact": {
                    "poor_metabolizer": "Increased exposure → Enhanced acid suppression (may be beneficial, reduce dose).",
                    "ultra_rapid_metabolizer": "Reduced efficacy → H. pylori eradication rates decreased. Increase dose.",
                    "normal_metabolizer": "Standard response expected."
                },
                "recommendation": "Increase dose 2-3x in ultra-rapid metabolizers for H. pylori."
            },
            "diazepam": {
                "level": "2A",
                "guideline": "DPWG",
                "phenotype_impact": {
                    "poor_metabolizer": "Prolonged sedation → Reduce dose by 50% or use lorazepam/oxazepam.",
                    "ultra_rapid_metabolizer": "Reduced duration of action. May need dose adjustment.",
                    "normal_metabolizer": "Standard response expected."
                },
                "recommendation": "Use lorazepam in poor metabolizers (not CYP2C19 dependent)."
            },
            "sertraline": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "Increased exposure → Consider 50% dose reduction.",
                    "ultra_rapid_metabolizer": "Decreased exposure → Consider alternative SSRI or dose increase.",
                    "normal_metabolizer": "Standard response expected."
                },
                "recommendation": "Reduce dose in poor metabolizers; consider alternative in ultra-rapid."
            },
            "warfarin": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "Adjusted dose algorithm recommended. Increased sensitivity.",
                    "normal_metabolizer": "Standard dosing algorithm."
                },
                "recommendation": "Use pharmacogenomic dosing algorithm (CYP2C19 + CYP2C9 + VKORC1)."
            },
        }
    },

    # ── CYP2C9 ──
    "CYP2C9": {
        "gene_name": "Cytochrome P450 2C9",
        "chromosome": "10q23.33",
        "function": "Metabolism of warfarin, NSAIDs, and sulfonylureas",
        "drugs": {
            "warfarin": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "CRITICAL: 5-10x increased bleeding risk. Dramatically reduce starting dose.",
                    "intermediate_metabolizer": "Increased sensitivity — reduce dose ~30-40%.",
                    "normal_metabolizer": "Standard dosing per clinical algorithm."
                },
                "recommendation": "Use FDA-approved pharmacogenomic dosing table. CYP2C9 *2/*3 carriers need 20-80% dose reduction."
            },
            "ibuprofen": {
                "level": "2A",
                "guideline": "DPWG",
                "phenotype_impact": {
                    "poor_metabolizer": "Increased AUC → Higher GI bleeding and renal risk.",
                    "normal_metabolizer": "Standard response."
                },
                "recommendation": "Consider dose reduction or alternative NSAID in CYP2C9 poor metabolizers."
            },
            "celecoxib": {
                "level": "1B",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "3-7x increased exposure → Reduce dose by 50%.",
                    "intermediate_metabolizer": "2x increased exposure → Consider dose adjustment.",
                    "normal_metabolizer": "Standard response."
                },
                "recommendation": "Reduce starting dose by 50% in CYP2C9 poor metabolizers."
            },
        }
    },

    # ── SLCO1B1 ──
    "SLCO1B1": {
        "gene_name": "Solute Carrier Organic Anion Transporter 1B1",
        "chromosome": "12p12.1",
        "function": "Hepatic uptake of statins and other drugs",
        "drugs": {
            "simvastatin": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "decreased_function": "CRITICAL: 2.6x increased myopathy risk. Maximum dose 20mg. Consider rosuvastatin.",
                    "poor_function": "CONTRAINDICATED at >20mg. Switch to pravastatin or rosuvastatin.",
                    "normal_function": "Standard dosing. Monitor CK levels."
                },
                "recommendation": "Limit to 20mg in SLCO1B1 *5 carriers. Use pravastatin/rosuvastatin as alternatives."
            },
            "atorvastatin": {
                "level": "2A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "decreased_function": "Mildly increased myopathy risk vs simvastatin. Monitor.",
                    "normal_function": "Standard response."
                },
                "recommendation": "Preferred over simvastatin in SLCO1B1 variant carriers."
            },
        }
    },

    # ── VKORC1 ──
    "VKORC1": {
        "gene_name": "Vitamin K Epoxide Reductase Complex Subunit 1",
        "chromosome": "16p11.2",
        "function": "Target enzyme of warfarin — vitamin K recycling",
        "drugs": {
            "warfarin": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "high_sensitivity": "CRITICAL: -1639 G>A carriers need 25-50% dose reduction. Over-anticoagulation risk.",
                    "normal_sensitivity": "Standard dosing algorithm."
                },
                "recommendation": "Combine VKORC1 + CYP2C9 genotype for pharmacogenomic warfarin dosing."
            },
        }
    },

    # ── HLA-B ──
    "HLA-B": {
        "gene_name": "Human Leukocyte Antigen B",
        "chromosome": "6p21.3",
        "function": "Immune system antigen presentation — drug hypersensitivity reactions",
        "drugs": {
            "carbamazepine": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "HLA-B*15:02_positive": "CRITICAL: Stevens-Johnson Syndrome / Toxic Epidermal Necrolysis risk. CONTRAINDICATED.",
                    "HLA-B*15:02_negative": "Standard risk."
                },
                "recommendation": "Screen HLA-B*15:02 before prescribing (FDA requirement). Use alternative anticonvulsant if positive."
            },
            "allopurinol": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "HLA-B*58:01_positive": "CRITICAL: Severe cutaneous adverse reaction risk. CONTRAINDICATED.",
                    "HLA-B*58:01_negative": "Standard risk."
                },
                "recommendation": "Screen HLA-B*58:01 before prescribing. Use febuxostat if positive."
            },
            "abacavir": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "HLA-B*57:01_positive": "CRITICAL: Hypersensitivity reaction. CONTRAINDICATED. Use alternative NRTI.",
                    "HLA-B*57:01_negative": "Standard risk — can prescribe."
                },
                "recommendation": "MANDATORY HLA-B*57:01 screening before abacavir (FDA boxed warning)."
            },
        }
    },

    # ── DPYD ──
    "DPYD": {
        "gene_name": "Dihydropyrimidine Dehydrogenase",
        "chromosome": "1p21.3",
        "function": "Rate-limiting enzyme in 5-fluorouracil catabolism",
        "drugs": {
            "fluorouracil": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "CRITICAL: Life-threatening toxicity (mucositis, neutropenia, death). Reduce dose 50% or use alternative.",
                    "intermediate_metabolizer": "Increased toxicity risk. Reduce dose 25-50%.",
                    "normal_metabolizer": "Standard dosing."
                },
                "recommendation": "Pre-treatment DPYD genotyping recommended (EMA mandate in EU). Reduce dose based on activity score."
            },
            "capecitabine": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "CRITICAL: Prodrug of 5-FU — same severe toxicity risk. Reduce dose 50%+.",
                    "intermediate_metabolizer": "Reduce dose 25-50%.",
                    "normal_metabolizer": "Standard dosing."
                },
                "recommendation": "Screen DPYD before prescribing capecitabine."
            },
        }
    },

    # ── TPMT ──
    "TPMT": {
        "gene_name": "Thiopurine S-methyltransferase",
        "chromosome": "6p22.3",
        "function": "Inactivation of thiopurine drugs (azathioprine, 6-MP)",
        "drugs": {
            "azathioprine": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "CRITICAL: Fatal myelosuppression risk. Reduce dose by 90% or use alternative.",
                    "intermediate_metabolizer": "Increased myelotoxicity. Reduce starting dose by 30-70%.",
                    "normal_metabolizer": "Standard dosing with WBC monitoring."
                },
                "recommendation": "TPMT genotype/phenotype testing before thiopurine initiation."
            },
            "mercaptopurine": {
                "level": "1A",
                "guideline": "CPIC",
                "phenotype_impact": {
                    "poor_metabolizer": "CRITICAL: Fatal myelosuppression. Reduce dose >90%.",
                    "intermediate_metabolizer": "Significant myelotoxicity risk. Reduce 30-70%.",
                    "normal_metabolizer": "Standard dosing."
                },
                "recommendation": "Mandatory TPMT testing in pediatric ALL protocols."
            },
        }
    },
}

# Convenience: flat lookup drug → [gene evidence entries]
DRUG_TO_PGX = {}
for gene, gene_data in PGX_EVIDENCE_DB.items():
    for drug_name, drug_entry in gene_data["drugs"].items():
        if drug_name not in DRUG_TO_PGX:
            DRUG_TO_PGX[drug_name] = []
        DRUG_TO_PGX[drug_name].append({
            "gene": gene,
            "gene_name": gene_data["gene_name"],
            "chromosome": gene_data["chromosome"],
            "evidence_level": drug_entry["level"],
            "guideline": drug_entry["guideline"],
            "recommendation": drug_entry["recommendation"],
            "phenotype_impact": drug_entry["phenotype_impact"]
        })


def get_pgx_evidence(drug_name):
    """Look up all PGx evidence for a drug."""
    key = drug_name.lower().strip()
    entries = DRUG_TO_PGX.get(key, [])
    return {
        "drug": drug_name,
        "total_markers": len(entries),
        "evidence": entries
    }


def get_gene_info(gene_name):
    """Get full info for a specific gene."""
    gene = PGX_EVIDENCE_DB.get(gene_name.upper().strip())
    if not gene:
        return {"error": f"Gene {gene_name} not in database"}
    return gene


def get_patient_pgx_report(drugs, patient_genetics):
    """
    Given a list of drugs and a patient's genetic profile,
    return all actionable PGx warnings with evidence levels.
    
    patient_genetics example: {"CYP2D6": "poor_metabolizer", "CYP2C19": "ultra_rapid_metabolizer"}
    """
    warnings = []
    for drug in drugs:
        entries = DRUG_TO_PGX.get(drug.lower().strip(), [])
        for entry in entries:
            gene = entry["gene"]
            patient_status = patient_genetics.get(gene)
            if patient_status and patient_status in entry["phenotype_impact"]:
                impact = entry["phenotype_impact"][patient_status]
                severity = "critical" if "CRITICAL" in impact or "CONTRAINDICATED" in impact else "warning"
                warnings.append({
                    "drug": drug,
                    "gene": gene,
                    "gene_name": entry["gene_name"],
                    "patient_status": patient_status,
                    "evidence_level": entry["evidence_level"],
                    "guideline": entry["guideline"],
                    "impact": impact,
                    "recommendation": entry["recommendation"],
                    "severity": severity
                })
    
    # Sort: critical first, then by evidence level
    level_order = {"1A": 0, "1B": 1, "2A": 2, "2B": 3, "3": 4, "4": 5}
    warnings.sort(key=lambda w: (0 if w["severity"] == "critical" else 1, level_order.get(w["evidence_level"], 9)))
    
    return {
        "total_warnings": len(warnings),
        "actionable_count": sum(1 for w in warnings if w["evidence_level"] in ("1A", "1B")),
        "warnings": warnings
    }
