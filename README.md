# odoo-af — gren 19.0

> **Denna gren är avsiktligt tom.** Modulerna är INTE portade till Odoo 19.
> Grenen finns så att dev-miljöer (`hansolo19`) kan klona den utan att falla,
> men den påstår ingenting om att koden är portad.

## Baseline

| | |
|---|---|
| Källa | `12.0-test (senaste versionsgren)` |
| Moduler | **14** |
| Grenar i repot | `12.0`, `12.0-2249`, `12.0-AFC-125_Mass-mailing-template-enhancements`, `12.0-AFC-1725b_ImprovementsTemplates`, `12.0-AFC-1804_Install_All_modul`, `12.0-AFC-2306`, `12.0-AFC-2325`, `12.0-AFC-2350`, `12.0-AFC-2424-remove-ADKD-Editor`, `12.0-AFC-2474`, `12.0-AFC-2534`, `12.0-AFC-3028_user_group`, `12.0-AFC-3077`, `12.0-DAFA-AFC-1806_InstallAllModule`, `12.0-af`, `12.0-af-mass-mailing-template`, `12.0-test`, `AFC-3127-IPF-Genomforande`, `Dev-12.0`, `Dev-12.0-AFC-2375-quicklink_for_partners`, `Dev-12.0-Fenix-Sprint-02`, `master`, `revert-729-12.0-AFC-3028`, `revert-732-12.0-AFC-3028_user_group` |

## Moduler

- `af_backend_tema`
- `af_base_demo`
- `af_bugherd`
- `af_data_ais-f_loader`
- `af_demodata`
- `af_install_modules`
- `af_rest_appointment`
- `af_rest_core`
- `af_security`
- `base_afdemo`
- `calendar_af`
- `calender_timereport`
- `test_data_af`
- `test_data_demo_sv`

## Blockerare

**10 externa beroenden saknas** i Odoo 19-kärnan och OCA 19.0:

| Beroende | Behövs av |
|---|---|
| `hr_timesheet_sheet` | `calender_timereport` |
| `partner_daily_notes` | `af_data_ais-f_loader`, `af_install_modules`, `af_security`, `test_data_af` |
| `partner_desired_jobs` | `af_data_ais-f_loader`, `af_install_modules`, `test_data_af` |
| `partner_employee360` | `af_rest_appointment` |
| `partner_kpi_data` | `af_data_ais-f_loader`, `af_install_modules`, `test_data_af` |
| `partner_view_360` | `af_data_ais-f_loader`, `af_install_modules`, `af_security`, `calendar_af` … |
| `res_drivers_license` | `af_data_ais-f_loader`, `af_install_modules`, `test_data_af` |
| `res_sni` | `af_data_ais-f_loader`, `af_install_modules`, `test_data_af` |
| `res_ssyk` | `af_data_ais-f_loader`, `af_install_modules`, `test_data_af` |
| `res_sun` | `af_data_ais-f_loader`, `af_install_modules`, `test_data_af` |

### Prioritering

Ett beroende som blockerar många moduler ger mest nytta att lösa först:

- `partner_view_360` — frisläpper **5** modul(er)
- `partner_daily_notes` — frisläpper **4** modul(er)
- `partner_desired_jobs` — frisläpper **3** modul(er)
- `partner_kpi_data` — frisläpper **3** modul(er)
- `res_drivers_license` — frisläpper **3** modul(er)

## Nästa steg

Portering sker på `*-pfile`-maskin med versionsagnostisk kod
(`.p.py` / `.p.xml`). Se `/skill:odoo-pfiles`.
