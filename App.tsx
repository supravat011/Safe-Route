import React, { useState, useEffect } from 'react';
import {
    Menu, X, ShieldAlert, Map as MapIcon,
    FileText, Activity, Phone, ShieldCheck,
    LayoutDashboard, AlertTriangle, ChevronRight,
    Upload, Camera, MapPin, Siren,
    Search, ExternalLink, RefreshCw, Zap
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { AccidentReport, AccidentType, PageView, Severity } from './types';
import { MOCK_HOSPITALS, MOCK_REPORTS, STATIC_SAFETY_TIPS } from './constants';
import { analyzeAccidentReport, getSafetyAdvice } from './services/geminiService';

// --- Sub-components ---

// 1. Navigation Component
const Navbar = ({ activePage, setPage, isMobileMenuOpen, setIsMobileMenuOpen }: any) => {
    const navItems = [
        { id: PageView.HOME, label: 'Home', icon: <ShieldCheck size={16} /> },
        { id: PageView.REPORT, label: 'Report', icon: <FileText size={16} /> },
        { id: PageView.MAP, label: 'Live Map', icon: <MapIcon size={16} /> },
        { id: PageView.SAFETY, label: 'Safety', icon: <Activity size={16} /> },
        { id: PageView.EMERGENCY, label: 'SOS', icon: <Phone size={16} /> },
        { id: PageView.ADMIN, label: 'Admin', icon: <LayoutDashboard size={16} /> },
    ];

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 bg-black/50 backdrop-blur-xl border-b border-white/10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="flex items-center cursor-pointer gap-2" onClick={() => setPage(PageView.HOME)}>
                        <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2 rounded-lg shadow-[0_0_15px_rgba(37,99,235,0.5)]">
                            <ShieldAlert size={20} className="text-white" />
                        </div>
                        <span className="font-bold text-xl tracking-tight text-white">SAFE<span className="text-blue-500">ROUTE</span></span>
                    </div>

                    <div className="hidden md:flex items-center gap-1">
                        {navItems.map((item) => (
                            <button
                                key={item.id}
                                onClick={() => setPage(item.id)}
                                className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 flex items-center space-x-2 border border-transparent
                  ${activePage === item.id
                                        ? 'bg-zinc-800 text-white border-zinc-700 shadow-lg'
                                        : 'text-zinc-400 hover:text-white hover:bg-white/5'}`}
                            >
                                {item.icon}
                                <span>{item.label}</span>
                            </button>
                        ))}
                    </div>

                    <div className="flex md:hidden items-center">
                        <button
                            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                            className="p-2 rounded-md text-zinc-400 hover:text-white hover:bg-zinc-800 focus:outline-none"
                        >
                            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {isMobileMenuOpen && (
                <div className="md:hidden bg-zinc-950 border-b border-zinc-800">
                    <div className="px-4 pt-2 pb-6 space-y-1">
                        {navItems.map((item) => (
                            <button
                                key={item.id}
                                onClick={() => {
                                    setPage(item.id);
                                    setIsMobileMenuOpen(false);
                                }}
                                className={`w-full flex items-center space-x-3 px-3 py-3 rounded-lg text-base font-medium
                   ${activePage === item.id ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:bg-zinc-900 hover:text-white'}`}
                            >
                                {item.icon}
                                <span>{item.label}</span>
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </nav>
    );
};

// 2. Home Page
const HomePage = ({ setPage }: { setPage: (p: PageView) => void }) => {
    return (
        <div className="animate-in fade-in duration-700 min-h-screen pt-20 flex flex-col items-center">
            {/* Background Ambience */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[500px] opacity-30 pointer-events-none">
                <div className="absolute top-20 left-20 w-72 h-72 bg-blue-600 rounded-full blur-[100px] mix-blend-screen animate-pulse"></div>
                <div className="absolute top-40 right-20 w-96 h-96 bg-purple-600 rounded-full blur-[100px] mix-blend-screen opacity-70"></div>
            </div>

            <div className="relative max-w-5xl mx-auto px-4 py-20 sm:px-6 lg:px-8 flex flex-col items-center text-center z-10">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-blue-500/30 bg-blue-500/10 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-6">
                    <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span> Live System Active
                </div>

                <h1 className="text-5xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-b from-white via-white to-zinc-500 tracking-tight mb-6 leading-tight">
                    Report Accidents. <br />
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-500">Save Lives.</span>
                </h1>

                <p className="mt-4 max-w-2xl text-lg md:text-xl text-zinc-400 font-light leading-relaxed">
                    A next-generation real-time platform for safer roads. Leverage AI to report incidents instantly and coordinate emergency response.
                </p>

                <div className="mt-10 flex flex-col sm:flex-row gap-5 w-full sm:w-auto">
                    <button
                        onClick={() => setPage(PageView.REPORT)}
                        className="group relative px-8 py-4 bg-white text-black font-semibold rounded-full shadow-[0_0_20px_rgba(255,255,255,0.3)] hover:shadow-[0_0_30px_rgba(255,255,255,0.5)] transition-all transform hover:-translate-y-1 overflow-hidden"
                    >
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-zinc-200 to-transparent opacity-0 group-hover:opacity-100 transform -translate-x-full group-hover:translate-x-full transition-all duration-700"></div>
                        <span className="flex items-center justify-center gap-2 relative z-10">
                            <ShieldAlert size={18} /> Report Accident
                        </span>
                    </button>
                    <button
                        onClick={() => setPage(PageView.MAP)}
                        className="px-8 py-4 bg-zinc-900 text-white border border-zinc-800 hover:border-zinc-600 hover:bg-zinc-800 font-semibold rounded-full transition-all transform hover:-translate-y-1 flex items-center justify-center gap-2"
                    >
                        <MapIcon size={18} /> View Live Map
                    </button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="max-w-7xl mx-auto px-4 w-full relative z-10 mb-20">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-zinc-900/40 backdrop-blur-md p-6 rounded-2xl border border-white/10 hover:border-blue-500/50 transition-colors group">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-xs font-medium text-zinc-500 uppercase tracking-widest mb-1">Today's Reports</p>
                                <p className="text-4xl font-bold text-white group-hover:text-blue-400 transition-colors">124</p>
                            </div>
                            <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
                                <FileText size={20} />
                            </div>
                        </div>
                    </div>
                    <div className="bg-zinc-900/40 backdrop-blur-md p-6 rounded-2xl border border-white/10 hover:border-red-500/50 transition-colors group">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-xs font-medium text-zinc-500 uppercase tracking-widest mb-1">Active Alerts</p>
                                <p className="text-4xl font-bold text-white group-hover:text-red-400 transition-colors">18</p>
                            </div>
                            <div className="p-2 bg-red-500/10 rounded-lg text-red-400">
                                <AlertTriangle size={20} />
                            </div>
                        </div>
                    </div>
                    <div className="bg-zinc-900/40 backdrop-blur-md p-6 rounded-2xl border border-white/10 hover:border-yellow-500/50 transition-colors group">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-xs font-medium text-zinc-500 uppercase tracking-widest mb-1">Risk Zones</p>
                                <p className="text-4xl font-bold text-white group-hover:text-yellow-400 transition-colors">5</p>
                            </div>
                            <div className="p-2 bg-yellow-500/10 rounded-lg text-yellow-400">
                                <Zap size={20} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// 3. Report Accident Page
const ReportPage = () => {
    const [loading, setLoading] = useState(false);
    const [description, setDescription] = useState('');
    const [aiAnalysis, setAiAnalysis] = useState<{ severity: string, summary: string } | null>(null);
    const [submitted, setSubmitted] = useState(false);

    const handleAnalyze = async () => {
        if (!description) return;
        setLoading(true);
        const result = await analyzeAccidentReport(description);
        setAiAnalysis(result);
        setLoading(false);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setSubmitted(true);
        setTimeout(() => {
            setSubmitted(false);
            setDescription('');
            setAiAnalysis(null);
        }, 3000);
    };

    if (submitted) {
        return (
            <div className="flex items-center justify-center min-h-[60vh] pt-20">
                <div className="text-center p-10 bg-zinc-900/50 backdrop-blur-xl rounded-3xl border border-emerald-500/30 shadow-[0_0_50px_-12px_rgba(16,185,129,0.2)] max-w-md mx-auto animate-in zoom-in duration-500">
                    <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-emerald-500/10 mb-6 relative">
                        <div className="absolute inset-0 bg-emerald-500/20 rounded-full animate-ping"></div>
                        <ShieldCheck size={40} className="text-emerald-500 relative z-10" />
                    </div>
                    <h2 className="text-3xl font-bold text-white mb-3">Report Submitted</h2>
                    <p className="text-zinc-400 leading-relaxed">Thank you. Emergency services have been notified and help is on the way.</p>
                    <button onClick={() => setSubmitted(false)} className="mt-8 px-6 py-2 rounded-full border border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10 transition-colors text-sm font-medium">Submit Another</button>
                </div>
            </div>
        );
    }

    return (
        <div className="pt-24 pb-12 max-w-3xl mx-auto px-4 animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="bg-zinc-900/50 backdrop-blur-xl rounded-3xl border border-white/10 shadow-2xl overflow-hidden relative">
                {/* Glow effect */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-red-600/10 rounded-full blur-[80px] pointer-events-none"></div>

                <div className="p-8 border-b border-white/5 flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-bold text-white tracking-tight">Report Incident</h2>
                        <p className="text-zinc-500 text-sm mt-1">Provide accurate details for faster response.</p>
                    </div>
                    <div className="w-10 h-10 rounded-full bg-red-500/10 flex items-center justify-center">
                        <AlertTriangle className="text-red-500" size={20} />
                    </div>
                </div>

                <div className="p-8">
                    <div className="mb-8 p-4 bg-red-950/30 border border-red-500/20 rounded-xl flex gap-3">
                        <AlertTriangle className="text-red-500 shrink-0 mt-0.5" size={18} />
                        <p className="text-red-200/80 text-sm leading-relaxed">
                            <span className="font-semibold text-red-400">Legal Warning:</span> False reporting is a criminal offense. Please ensure all provided information is accurate to the best of your knowledge.
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Location</label>
                                <div className="relative group">
                                    <input type="text" placeholder="Landmark or road name" className="w-full pl-10 pr-28 py-4 bg-black/40 border border-zinc-800 rounded-xl text-white placeholder-zinc-600 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all" required />
                                    <MapPin className="absolute left-3 top-4 text-zinc-500 group-focus-within:text-blue-500 transition-colors" size={18} />
                                    <button type="button" className="absolute right-2 top-2 bottom-2 px-3 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors border border-zinc-700">
                                        <Siren size={12} className="text-blue-400" /> Auto-Locate
                                    </button>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Accident Type</label>
                                <div className="relative">
                                    <select className="w-full px-4 py-4 bg-black/40 border border-zinc-800 rounded-xl text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none appearance-none transition-all">
                                        {Object.values(AccidentType).map(t => <option key={t} value={t} className="bg-zinc-900">{t}</option>)}
                                    </select>
                                    <ChevronRight className="absolute right-4 top-4 text-zinc-500 rotate-90" size={18} />
                                </div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Description</label>
                            <textarea
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                rows={4}
                                className="w-full px-4 py-4 bg-black/40 border border-zinc-800 rounded-xl text-white placeholder-zinc-600 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all resize-none"
                                placeholder="Describe the incident (vehicles involved, injuries, blocked lanes...)"
                            />
                            <div className="flex justify-end">
                                <button
                                    type="button"
                                    onClick={handleAnalyze}
                                    disabled={loading || !description}
                                    className="mt-2 text-xs flex items-center gap-2 text-blue-400 font-medium hover:text-blue-300 disabled:opacity-50 transition-colors px-3 py-1.5 rounded-lg hover:bg-blue-500/10"
                                >
                                    {loading ? <RefreshCw className="animate-spin" size={12} /> : <Activity size={12} />}
                                    Analyze Severity with Gemini AI
                                </button>
                            </div>
                        </div>

                        {/* AI Analysis Result */}
                        {aiAnalysis && (
                            <div className="bg-indigo-950/30 border border-indigo-500/30 rounded-xl p-5 animate-in fade-in slide-in-from-top-2">
                                <div className="flex items-start gap-4">
                                    <div className="p-2 bg-indigo-500/20 rounded-lg text-indigo-400">
                                        <ShieldCheck size={18} />
                                    </div>
                                    <div>
                                        <h4 className="font-semibold text-indigo-200">AI Assessment</h4>
                                        <p className="text-sm text-indigo-300/80 mt-1">Suggested Severity: <span className="font-bold uppercase text-white tracking-wide">{aiAnalysis.severity}</span></p>
                                        <p className="text-xs text-indigo-400 mt-2 italic border-l-2 border-indigo-500/30 pl-3">"{aiAnalysis.summary}"</p>
                                    </div>
                                </div>
                            </div>
                        )}

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Severity Level</label>
                                <div className="relative">
                                    <select
                                        defaultValue={aiAnalysis?.severity || Severity.MEDIUM}
                                        className="w-full px-4 py-4 bg-black/40 border border-zinc-800 rounded-xl text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none appearance-none"
                                    >
                                        {Object.values(Severity).map(s => <option key={s} value={s} className="bg-zinc-900">{s}</option>)}
                                    </select>
                                    <ChevronRight className="absolute right-4 top-4 text-zinc-500 rotate-90" size={18} />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Evidence (Optional)</label>
                                <label className="flex items-center justify-center w-full h-[58px] border border-dashed border-zinc-700 rounded-xl hover:bg-zinc-800/50 hover:border-zinc-500 cursor-pointer group transition-all">
                                    <Camera className="mr-2 text-zinc-500 group-hover:text-white transition-colors" size={18} />
                                    <span className="text-sm text-zinc-500 group-hover:text-zinc-300 transition-colors">Upload Photo</span>
                                    <input type="file" className="hidden" accept="image/*" />
                                </label>
                            </div>
                        </div>

                        <button type="submit" className="w-full py-4 bg-white text-black font-bold rounded-xl hover:bg-zinc-200 transition-all transform hover:scale-[1.01] text-lg shadow-[0_0_20px_rgba(255,255,255,0.1)]">
                            Submit Report
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

// 4. Live Map (Mock)
const LiveMapPage = () => {
    return (
        <div className="h-screen w-full relative bg-black overflow-hidden pt-16">
            {/* Dark Map Style */}
            <div className="absolute inset-0 opacity-20"
                style={{ backgroundImage: 'linear-gradient(#333 1px, transparent 1px), linear-gradient(90deg, #333 1px, transparent 1px)', backgroundSize: '40px 40px' }}>
            </div>

            {/* Map Roads */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-30">
                <path d="M-100,200 Q400,250 800,100 T1600,300" stroke="#52525b" strokeWidth="20" fill="none" />
                <path d="M200,-100 L300,1000" stroke="#52525b" strokeWidth="15" fill="none" />
                <path d="M800,0 L750,900" stroke="#52525b" strokeWidth="15" fill="none" />
            </svg>

            {/* Controls Overlay */}
            <div className="absolute top-20 left-4 right-4 md:left-auto md:right-8 md:w-80 bg-zinc-900/80 backdrop-blur-xl p-5 rounded-2xl border border-white/10 shadow-2xl z-10">
                <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div> Live Incidents
                </h3>
                <div className="space-y-3">
                    <label className="flex items-center gap-3 text-sm text-zinc-300 cursor-pointer hover:text-white transition-colors">
                        <div className="w-4 h-4 rounded border border-zinc-600 flex items-center justify-center bg-blue-600 border-transparent">✓</div> High Severity
                    </label>
                    <label className="flex items-center gap-3 text-sm text-zinc-300 cursor-pointer hover:text-white transition-colors">
                        <div className="w-4 h-4 rounded border border-zinc-600 flex items-center justify-center bg-blue-600 border-transparent">✓</div> Recent (1h)
                    </label>
                </div>
                <div className="mt-5 pt-4 border-t border-white/10 grid grid-cols-2 gap-2">
                    <div className="flex items-center gap-2 text-xs text-zinc-400"><span className="w-2 h-2 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]"></span> High</div>
                    <div className="flex items-center gap-2 text-xs text-zinc-400"><span className="w-2 h-2 rounded-full bg-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.5)]"></span> Medium</div>
                    <div className="flex items-center gap-2 text-xs text-zinc-400"><span className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></span> Low</div>
                </div>
            </div>

            {/* Pins */}
            {MOCK_REPORTS.map((report, idx) => (
                <div
                    key={report.id}
                    className="absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer group z-0 hover:z-20"
                    style={{ top: `${30 + (idx * 15)}%`, left: `${20 + (idx * 20)}%` }}
                >
                    {/* Pulse Effect */}
                    {(report.severity === Severity.HIGH || report.severity === Severity.CRITICAL) && (
                        <div className="absolute inset-0 rounded-full bg-red-500/50 animate-ping"></div>
                    )}

                    <div className={`
            relative flex items-center justify-center w-8 h-8 rounded-full shadow-lg border-2 border-black
            ${report.severity === Severity.HIGH || report.severity === Severity.CRITICAL ? 'bg-red-500 text-white' :
                            report.severity === Severity.MEDIUM ? 'bg-yellow-500 text-black' : 'bg-emerald-500 text-black'}
            transition-transform duration-300 group-hover:scale-125
          `}>
                        <MapIcon size={14} />
                    </div>

                    {/* Tooltip Card */}
                    <div className="absolute bottom-12 left-1/2 -translate-x-1/2 w-72 bg-zinc-900/95 backdrop-blur-md rounded-xl border border-white/10 shadow-2xl p-4 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-2 group-hover:translate-y-0 pointer-events-none">
                        <div className="flex items-center justify-between mb-2">
                            <span className="px-2 py-0.5 rounded-md bg-white/10 text-[10px] font-bold uppercase tracking-wider text-white border border-white/5">{report.type}</span>
                            <span className={`text-[10px] font-bold uppercase ${report.severity === Severity.HIGH ? 'text-red-400' : 'text-zinc-400'}`}>{report.severity}</span>
                        </div>
                        <p className="text-sm text-zinc-300 leading-snug mb-3">{report.description}</p>
                        <div className="flex items-center gap-2 text-xs text-zinc-500 border-t border-white/5 pt-2">
                            <Activity size={12} />
                            <span>{new Date(report.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

// 5. Safety Awareness
const SafetyPage = () => {
    const [activeTab, setActiveTab] = useState('rules');
    const [aiQuestion, setAiQuestion] = useState('');
    const [aiAnswer, setAiAnswer] = useState('');
    const [loading, setLoading] = useState(false);

    const askAi = async () => {
        if (!aiQuestion) return;
        setLoading(true);
        const answer = await getSafetyAdvice(aiQuestion);
        setAiAnswer(answer);
        setLoading(false);
    }

    return (
        <div className="pt-24 pb-12 max-w-7xl mx-auto px-4 animate-in fade-in duration-700">
            <div className="text-center mb-16">
                <h2 className="text-4xl font-bold text-white mb-4">Road Safety Awareness</h2>
                <p className="text-zinc-400 max-w-2xl mx-auto text-lg font-light">
                    Stay informed with the latest traffic rules and get instant safety advice powered by AI.
                </p>
            </div>

            {/* AI Assistant Section */}
            <div className="relative mb-20">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-3xl blur-3xl -z-10"></div>
                <div className="bg-zinc-900/60 backdrop-blur-xl rounded-3xl p-8 md:p-12 border border-white/10 shadow-2xl flex flex-col lg:flex-row gap-10 items-start">
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400">
                                <RefreshCw className={loading ? "animate-spin" : ""} size={20} />
                            </div>
                            <h3 className="text-2xl font-bold text-white">AI Safety Assistant</h3>
                        </div>
                        <p className="text-zinc-400 mb-8 leading-relaxed">
                            Not sure about a specific traffic rule or safety guideline? Our AI model is trained on global road safety standards to provide you with instant, accurate answers.
                        </p>

                        <div className={`p-6 rounded-2xl border transition-all duration-500 ${aiAnswer ? 'bg-zinc-800/50 border-blue-500/30' : 'bg-black/20 border-white/5 border-dashed'}`}>
                            {aiAnswer ? (
                                <p className="text-lg text-zinc-100 leading-relaxed">{aiAnswer}</p>
                            ) : (
                                <p className="text-zinc-500 italic flex items-center gap-2">
                                    <Zap size={16} /> try: "What should I do if my brakes fail?"
                                </p>
                            )}
                        </div>
                    </div>

                    <div className="w-full lg:w-[400px] flex flex-col gap-4">
                        <div className="relative">
                            <input
                                type="text"
                                value={aiQuestion}
                                onChange={(e) => setAiQuestion(e.target.value)}
                                placeholder="Type your question..."
                                className="w-full pl-5 pr-4 py-4 bg-black/50 border border-zinc-700 rounded-xl text-white placeholder-zinc-600 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                            />
                        </div>
                        <button
                            onClick={askAi}
                            disabled={loading}
                            className="w-full py-4 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl transition-all shadow-[0_0_20px_rgba(37,99,235,0.3)] disabled:opacity-50 disabled:shadow-none"
                        >
                            {loading ? 'Thinking...' : 'Get Answer'}
                        </button>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {STATIC_SAFETY_TIPS.map((tip, idx) => (
                    <div key={idx} className="bg-zinc-900/40 border border-zinc-800 p-8 rounded-2xl hover:border-emerald-500/50 hover:bg-zinc-900/60 transition-all duration-300 group">
                        <div className="flex items-center justify-between mb-4">
                            <h4 className="font-bold text-lg text-zinc-100 group-hover:text-emerald-400 transition-colors">{tip.title}</h4>
                            <span className={`px-2 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider
                  ${tip.category === 'Warning' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'}
               `}>{tip.category}</span>
                        </div>
                        <p className="text-zinc-400 text-sm leading-relaxed group-hover:text-zinc-300 transition-colors">{tip.content}</p>
                    </div>
                ))}
                {/* Skeleton Card */}
                <div className="bg-zinc-900/20 border border-zinc-800 border-dashed p-8 rounded-2xl flex items-center justify-center text-zinc-600">
                    More tips loading...
                </div>
            </div>
        </div>
    );
};

// 6. Emergency & Hospitals
const EmergencyPage = () => {
    return (
        <div className="pt-24 pb-12 max-w-5xl mx-auto px-4 animate-in fade-in duration-700">
            <div className="bg-gradient-to-b from-red-600 to-red-700 text-white p-12 rounded-3xl shadow-[0_0_50px_-10px_rgba(220,38,38,0.5)] mb-12 text-center relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-full bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB3aWR0aD0iNCIgaGVpZ2h0PSI0IiBmaWxsPSIjZmZmIiBmaWxsLW9wYWNpdHk9IjAuMDUiLz4KPC9zdmc+')] opacity-30"></div>
                <h2 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight relative z-10">EMERGENCY SOS</h2>
                <p className="text-red-100 mb-10 text-lg relative z-10">Pressing these buttons will immediately connect you to emergency services.</p>
                <div className="flex flex-col sm:flex-row justify-center gap-6 relative z-10">
                    <button className="group flex-1 bg-white text-red-600 px-8 py-6 rounded-2xl font-bold text-xl shadow-xl hover:bg-zinc-100 transition-all transform hover:-translate-y-1 flex items-center justify-center gap-4">
                        <div className="p-3 bg-red-100 rounded-full group-hover:bg-red-200 transition-colors">
                            <Phone size={24} className="fill-current" />
                        </div>
                        Call Ambulance (108)
                    </button>
                    <button className="group flex-1 bg-red-900 border border-red-800 text-white px-8 py-6 rounded-2xl font-bold text-xl shadow-xl hover:bg-red-950 transition-all transform hover:-translate-y-1 flex items-center justify-center gap-4">
                        <div className="p-3 bg-red-800 rounded-full group-hover:bg-red-700 transition-colors">
                            <ShieldAlert size={24} />
                        </div>
                        Call Police (100)
                    </button>
                </div>
            </div>

            <div className="flex items-center gap-3 mb-8">
                <div className="h-8 w-1 bg-blue-500 rounded-full"></div>
                <h3 className="text-2xl font-bold text-white">Nearby Help Centers</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {MOCK_HOSPITALS.map((hosp) => (
                    <div key={hosp.id} className="bg-zinc-900/50 p-6 rounded-2xl border border-white/5 hover:border-blue-500/30 transition-all group">
                        <div className="flex items-start justify-between mb-6">
                            <div className="flex items-center gap-4">
                                <div className={`p-3 rounded-xl ${hosp.type === 'Hospital' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-blue-500/10 text-blue-400'}`}>
                                    <Activity size={24} />
                                </div>
                                <div>
                                    <h4 className="font-bold text-lg text-white">{hosp.name}</h4>
                                    <p className="text-zinc-500 text-sm">{hosp.type}</p>
                                </div>
                            </div>
                            <span className="px-3 py-1 rounded-full bg-zinc-800 text-zinc-300 text-xs font-medium border border-zinc-700">{hosp.distance}</span>
                        </div>

                        <div className="flex gap-3">
                            <button className="flex-1 px-4 py-3 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl text-sm font-medium flex items-center justify-center gap-2 transition-colors">
                                <ExternalLink size={16} /> Directions
                            </button>
                            <button className="flex-1 px-4 py-3 bg-white hover:bg-zinc-200 text-black rounded-xl text-sm font-bold flex items-center justify-center gap-2 transition-colors">
                                <Phone size={16} /> {hosp.contact}
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

// 7. Admin Dashboard
const AdminDashboard = () => {
    const chartData = [
        { name: 'Jan', accidents: 40 },
        { name: 'Feb', accidents: 30 },
        { name: 'Mar', accidents: 55 },
        { name: 'Apr', accidents: 80 },
        { name: 'May', accidents: 65 },
        { name: 'Jun', accidents: 90 },
    ];

    const pieData = [
        { name: 'Collision', value: 400 },
        { name: 'Pedestrian', value: 300 },
        { name: 'Breakdown', value: 300 },
        { name: 'Other', value: 200 },
    ];

    const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

    return (
        <div className="min-h-screen bg-black flex flex-col md:flex-row pt-16">
            {/* Sidebar */}
            <div className="w-full md:w-72 bg-zinc-900/30 border-r border-white/5 p-6 hidden md:block">
                <h3 className="text-xs font-bold text-zinc-500 uppercase tracking-widest mb-6">Overview</h3>
                <ul className="space-y-2">
                    <li className="flex items-center gap-3 text-white bg-white/10 border border-white/5 px-4 py-3 rounded-xl font-medium"><LayoutDashboard size={18} /> Dashboard</li>
                    <li className="flex items-center gap-3 text-zinc-400 hover:text-white hover:bg-white/5 px-4 py-3 rounded-xl font-medium cursor-pointer transition-colors"><FileText size={18} /> Incident Reports</li>
                    <li className="flex items-center gap-3 text-zinc-400 hover:text-white hover:bg-white/5 px-4 py-3 rounded-xl font-medium cursor-pointer transition-colors"><MapPin size={18} /> Risk Zones</li>
                </ul>
            </div>

            <div className="flex-1 p-6 md:p-10 overflow-y-auto">
                <div className="flex justify-between items-center mb-10">
                    <h2 className="text-3xl font-bold text-white">System Status</h2>
                    <div className="flex items-center gap-2 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-emerald-400 text-xs font-bold uppercase">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div> Operational
                    </div>
                </div>

                {/* Widgets */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    {[
                        { label: 'Total Reports', value: '1,245', trend: '↑ 12%', color: 'text-blue-500' },
                        { label: 'Critical Severity', value: '42', trend: '↑ 5%', color: 'text-red-500' },
                        { label: 'Resolved Cases', value: '856', trend: '85% rate', color: 'text-emerald-500' },
                        { label: 'Avg Response', value: '12m', trend: '↓ 2m', color: 'text-yellow-500' },
                    ].map((widget, i) => (
                        <div key={i} className="bg-zinc-900/50 p-6 rounded-2xl border border-white/5 hover:border-white/10 transition-colors">
                            <div className="text-zinc-500 text-xs uppercase tracking-wider font-semibold mb-2">{widget.label}</div>
                            <div className="text-3xl font-bold text-white">{widget.value}</div>
                            <div className={`text-xs mt-3 font-medium ${widget.color}`}>{widget.trend}</div>
                        </div>
                    ))}
                </div>

                {/* Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    <div className="bg-zinc-900/50 p-6 rounded-2xl border border-white/5 h-96">
                        <h3 className="font-bold text-zinc-200 mb-6">Accident Trends</h3>
                        <ResponsiveContainer width="100%" height="85%">
                            <BarChart data={chartData}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#333" />
                                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#71717a' }} dy={10} />
                                <YAxis axisLine={false} tickLine={false} tick={{ fill: '#71717a' }} />
                                <Tooltip
                                    cursor={{ fill: '#27272a' }}
                                    contentStyle={{ backgroundColor: '#18181b', borderRadius: '12px', border: '1px solid #3f3f46', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)' }}
                                    itemStyle={{ color: '#fff' }}
                                />
                                <Bar dataKey="accidents" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="bg-zinc-900/50 p-6 rounded-2xl border border-white/5 h-96 flex flex-col">
                        <h3 className="font-bold text-zinc-200 mb-6">Incident Distribution</h3>
                        <div className="flex-1 flex items-center justify-center relative">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={pieData}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={80}
                                        outerRadius={100}
                                        paddingAngle={5}
                                        dataKey="value"
                                        stroke="none"
                                    >
                                        {pieData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip contentStyle={{ backgroundColor: '#18181b', borderRadius: '12px', border: '1px solid #3f3f46' }} itemStyle={{ color: '#fff' }} />
                                    <Legend verticalAlign="bottom" height={36} formatter={(value) => <span style={{ color: '#a1a1aa' }}>{value}</span>} />
                                </PieChart>
                            </ResponsiveContainer>
                            {/* Center text for donut chart */}
                            <div className="absolute inset-0 flex items-center justify-center pointer-events-none pb-12">
                                <div className="text-center">
                                    <span className="block text-3xl font-bold text-white">1.2k</span>
                                    <span className="text-xs text-zinc-500 uppercase">Total</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Recent Reports Table */}
                <div className="bg-zinc-900/50 rounded-2xl border border-white/5 overflow-hidden">
                    <div className="px-8 py-6 border-b border-white/5 flex justify-between items-center bg-white/5">
                        <h3 className="font-bold text-white">Recent Reports</h3>
                        <button className="text-blue-400 text-sm font-medium hover:text-blue-300">View All</button>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="text-zinc-500 font-medium bg-black/20">
                                <tr>
                                    <th className="px-8 py-4">ID</th>
                                    <th className="px-8 py-4">Type</th>
                                    <th className="px-8 py-4">Location</th>
                                    <th className="px-8 py-4">Severity</th>
                                    <th className="px-8 py-4">Status</th>
                                    <th className="px-8 py-4"></th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-zinc-800">
                                {MOCK_REPORTS.map((report) => (
                                    <tr key={report.id} className="hover:bg-white/5 transition-colors">
                                        <td className="px-8 py-4 font-mono text-zinc-400">#{report.id}</td>
                                        <td className="px-8 py-4 text-white font-medium">{report.type}</td>
                                        <td className="px-8 py-4 text-zinc-400">{report.location.address}</td>
                                        <td className="px-8 py-4">
                                            <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider border
                        ${report.severity === Severity.HIGH ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                                                    report.severity === Severity.MEDIUM ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'}`}>
                                                {report.severity}
                                            </span>
                                        </td>
                                        <td className="px-8 py-4">
                                            <span className="flex items-center gap-2 text-zinc-300">
                                                <span className={`w-1.5 h-1.5 rounded-full ${report.status === 'Resolved' ? 'bg-emerald-500' : 'bg-blue-500'}`}></span>
                                                {report.status}
                                            </span>
                                        </td>
                                        <td className="px-8 py-4 text-right">
                                            <button className="p-2 hover:bg-white/10 rounded-lg text-zinc-500 hover:text-white transition-colors">
                                                <ChevronRight size={16} />
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

// 8. Footer (Minimal)
const Footer = () => (
    <footer className="py-8 border-t border-white/5 mt-auto">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-6 text-zinc-500 text-sm">
            <div className="flex items-center gap-2">
                <span className="font-bold text-zinc-300 tracking-tight">SAFE ROUTE</span>
                <span className="w-1 h-1 bg-zinc-700 rounded-full"></span>
                <span>2024</span>
            </div>
            <div className="flex gap-8">
                <a href="#" className="hover:text-white transition-colors">Privacy</a>
                <a href="#" className="hover:text-white transition-colors">Terms</a>
                <a href="#" className="hover:text-white transition-colors">API</a>
            </div>
        </div>
    </footer>
);

// --- Main App Component ---

const App: React.FC = () => {
    const [activePage, setActivePage] = useState<PageView>(PageView.HOME);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    // Simple router switch
    const renderPage = () => {
        switch (activePage) {
            case PageView.HOME: return <HomePage setPage={setActivePage} />;
            case PageView.REPORT: return <ReportPage />;
            case PageView.MAP: return <LiveMapPage />;
            case PageView.SAFETY: return <SafetyPage />;
            case PageView.EMERGENCY: return <EmergencyPage />;
            case PageView.ADMIN: return <AdminDashboard />;
            default: return <HomePage setPage={setActivePage} />;
        }
    };

    return (
        <div className="min-h-screen flex flex-col font-sans bg-black text-zinc-100 selection:bg-blue-500/30 selection:text-blue-200">
            <Navbar
                activePage={activePage}
                setPage={setActivePage}
                isMobileMenuOpen={isMobileMenuOpen}
                setIsMobileMenuOpen={setIsMobileMenuOpen}
            />

            <main className="flex-grow flex flex-col">
                {renderPage()}
            </main>

            {/* Conditionally render footer */}
            {activePage !== PageView.MAP && activePage !== PageView.ADMIN && <Footer />}
        </div>
    );
};

export default App;