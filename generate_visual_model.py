from __future__ import annotations

from pathlib import Path


HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>一杯可乐放多少冰？</title>
  <style>
    :root {
      --bg: #f7f4ee;
      --panel: #fffdf8;
      --ink: #181817;
      --muted: #666059;
      --line: #d9d0c2;
      --blue: #1572a6;
      --red: #c7473f;
      --green: #487a55;
      --gold: #ad7419;
      --shadow: 0 14px 36px rgba(31, 25, 16, 0.10);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      color: var(--ink);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        linear-gradient(180deg, rgba(255,255,255,.82), rgba(247,244,238,.95)),
        radial-gradient(circle at top left, rgba(21,114,166,.14), transparent 34rem),
        var(--bg);
    }

    main {
      width: min(1120px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 34px 0 42px;
    }

    header {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 22px;
      align-items: end;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--line);
    }

    h1 {
      margin: 0 0 8px;
      font-size: clamp(32px, 5vw, 58px);
      line-height: 1.04;
      letter-spacing: 0;
    }

    .lead {
      max-width: 760px;
      margin: 0;
      color: var(--muted);
      font-size: 17px;
      line-height: 1.65;
    }

    .fixed {
      min-width: 260px;
      padding: 14px 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,253,248,.72);
      color: var(--muted);
      line-height: 1.55;
      font-size: 14px;
    }

    .fixed strong {
      display: block;
      margin-bottom: 4px;
      color: var(--ink);
      font-size: 15px;
    }

    .hero {
      display: grid;
      grid-template-columns: minmax(280px, 360px) minmax(0, 1fr);
      gap: 18px;
      align-items: start;
      margin-top: 18px;
    }

    .left-stack {
      display: grid;
      gap: 18px;
    }

    .panel {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,253,248,.94);
      box-shadow: var(--shadow);
    }

    .control {
      padding: 22px;
    }

    .control label {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 14px;
      margin-bottom: 18px;
      font-weight: 760;
      font-size: 20px;
    }

    .control label span {
      color: var(--blue);
      font-size: 34px;
      line-height: 1;
      font-variant-numeric: tabular-nums;
      white-space: nowrap;
    }

    input[type="range"] {
      width: 100%;
      accent-color: var(--blue);
    }

    .ticks {
      display: flex;
      justify-content: space-between;
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
    }


    .cup-panel {
      display: grid;
      place-items: center;
      padding: 18px 18px 16px;
      min-height: 420px;
    }

    .cup-wrap {
      width: min(230px, 100%);
    }

    .cup-title {
      margin: 0 0 12px;
      text-align: center;
      font-size: 18px;
    }

    .cup-canvas {
      display: block;
      width: 100%;
      height: 318px;
      border: 0;
      background: transparent;
    }

    .cup-scale {
      display: grid;
      gap: 6px;
      margin-top: 14px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.35;
    }

    .bar {
      height: 9px;
      border-radius: 999px;
      overflow: hidden;
      background: #eadfce;
      border: 1px solid rgba(217,208,194,.82);
    }

    .bar span {
      display: block;
      height: 100%;
      width: 0%;
      border-radius: inherit;
      background: linear-gradient(90deg, var(--blue), #8fc3dd);
      transition: width .16s ease;
    }

    .metrics {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      align-content: start;
      gap: 12px;
      padding: 12px;
    }

    .metric {
      min-height: 142px;
      padding: 18px;
      border: 1px solid rgba(217,208,194,.78);
      border-radius: 7px;
      background: #fffdfa;
    }

    .metric b {
      display: block;
      margin-bottom: 10px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.35;
    }

    .metric strong {
      display: block;
      font-size: clamp(34px, 4.6vw, 50px);
      line-height: .96;
      font-variant-numeric: tabular-nums;
      white-space: nowrap;
    }

    .metric small {
      display: block;
      margin-top: 9px;
      color: var(--muted);
      line-height: 1.45;
      max-width: 18em;
    }

    .charts {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-top: 18px;
    }

    .chart {
      padding: 16px;
    }

    .chart h2 {
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }

    .chart canvas {
      display: block;
      width: 100%;
      height: 330px;
      border: 1px solid rgba(217,208,194,.78);
      border-radius: 6px;
      background: #fffdfa;
    }

    .legend {
      display: flex;
      flex-wrap: wrap;
      gap: 12px 18px;
      margin-top: 12px;
      color: var(--muted);
      font-size: 13px;
    }

    .key {
      display: inline-flex;
      align-items: center;
      gap: 7px;
    }

    .swatch {
      width: 22px;
      height: 3px;
      border-radius: 999px;
      background: var(--blue);
    }

    .swatch.red { background: var(--red); }
    .swatch.green { background: var(--green); }
    .swatch.gold { background: var(--gold); }

    .note {
      margin-top: 18px;
      padding: 18px 20px;
      color: var(--muted);
      line-height: 1.72;
    }

    .note p { margin: 0 0 10px; }
    .note p:last-child { margin-bottom: 0; }

    .modeling {
      margin-top: 18px;
      padding: 22px;
    }

    .modeling h2 {
      margin: 0 0 14px;
      font-size: 24px;
      line-height: 1.25;
    }

    .modeling-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;
    }

    .model-block {
      border: 1px solid rgba(217,208,194,.78);
      border-radius: 7px;
      background: #fffdfa;
      padding: 16px;
    }

    .model-block h3 {
      margin: 0 0 8px;
      font-size: 16px;
    }

    .model-block p {
      margin: 0;
      color: var(--muted);
      line-height: 1.7;
    }

    .formula {
      margin-top: 10px;
      padding: 10px 12px;
      border-radius: 6px;
      background: #f1eadf;
      color: #3a332b;
      font-size: 16px;
      line-height: 1.55;
      overflow-x: auto;
    }

    .formula math {
      display: block;
      margin: 2px auto;
      text-align: center;
    }

    .symbols {
      margin-top: 10px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.65;
    }

    @media (max-width: 940px) {
      header, .hero, .charts { grid-template-columns: 1fr; }
      .fixed { min-width: 0; }
      .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    @media (max-width: 560px) {
      main { width: min(100vw - 22px, 1120px); padding-top: 22px; }
      .chart canvas { height: 290px; }
      .cup-canvas { height: 300px; }
      .control label { display: block; }
      .control label span { display: block; margin-top: 8px; }
      .metrics { grid-template-columns: 1fr; }
    }

    @media (max-width: 390px) {
      .metrics { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>一杯可乐放多少冰？</h1>
        <p class="lead">只调一个变量：加入冰量。看杯子里的比例，再看 5 分钟后的温度、融冰量和浓度变化。</p>
      </div>
      <div class="fixed">
        <strong>固定条件</strong>
        可乐 300 g，初温 25°C；冰块 -18°C；室温 25°C；观察时间 5 分钟。
      </div>
    </header>

    <section class="hero">
      <div class="left-stack">
        <div class="panel control">
          <label for="iceMass">加入冰量 <span id="iceMassVal">180 g</span></label>
          <input id="iceMass" type="range" min="0" max="300" step="5" value="180" />
          <div class="ticks">
            <span>不加冰</span>
            <span>少冰</span>
            <span>正常冰</span>
            <span>满杯冰</span>
          </div>
          <p class="symbols">符号说明：Q 表示热量；k 是传热系数，用来近似接触面积、搅拌和杯壁等影响；T 是温度；m 是质量；Δt 是每一步模拟的时间间隔。下标 env、air、cola、ice 分别表示环境、空气、可乐和冰。</p>
        </div>

        <div class="panel cup-panel">
          <div class="cup-wrap">
            <h2 class="cup-title">杯子里的比例</h2>
            <div class="cup">
              <canvas class="cup-canvas" id="cupCanvas" width="320" height="430" aria-label="杯中可乐和浮冰物理示意图"></canvas>
            </div>
            <div class="cup-scale">
              <div>杯中按体积和浮力绘制，冰块大部分会浸在可乐里。</div>
              <div class="bar"><span id="iceVolumeBar"></span></div>
              <div id="cupCaption"></div>
            </div>
          </div>
          <p class="symbols">符号说明：ΔT 表示这一小段时间内可乐温度的变化；c 表示比热容，即 1 g 物质升高 1°C 需要的热量；m_liquid 是杯中液体总质量，由原来的可乐质量和已经融化的冰水质量相加得到。</p>
        </div>
      </div>

      <div class="panel metrics">
        <div class="metric">
          <b>5 分钟后温度</b>
          <strong id="tempMetric"></strong>
          <small id="tempNote"></small>
        </div>
        <div class="metric">
          <b>浓度</b>
          <strong id="dilutionMetric"></strong>
          <small>可乐 / (可乐 + 冰融化的水)。</small>
        </div>
      </div>
    </section>

    <section class="charts">
      <div class="panel chart">
        <h2>这杯可乐会怎么降温</h2>
        <canvas id="curveCanvas" width="760" height="420"></canvas>
        <div class="legend">
          <span class="key"><i class="swatch"></i>温度</span>
          <span class="key"><i class="swatch red"></i>浓度</span>
        </div>
      </div>
      <div class="panel chart">
        <h2>不同冰量的温度与浓度</h2>
        <canvas id="scanCanvas" width="760" height="420"></canvas>
        <div class="legend">
          <span class="key"><i class="swatch"></i>温度</span>
          <span class="key"><i class="swatch red"></i>浓度</span>
        </div>
      </div>
    </section>

    <section class="panel note">
      <p><strong>一句话：</strong>少冰不一定更浓。冰太少时，冰会融掉不少，但可乐仍然不够冷；冰足够多时，降温变快，融化量不会跟着冰量线性增加。</p>
      <p>这个页面使用的是简化热模型，适合解释趋势。真实结果会受杯子、冰块大小、搅拌、喝的速度和气泡逸出影响。</p>
    </section>

    <section class="panel modeling">
      <h2>完整数学建模过程</h2>
      <div class="modeling-grid">
        <div class="model-block">
          <h3>1. 建模对象与基本假设</h3>
          <p>研究对象是一杯可乐和若干冰块组成的开放热系统。模型只追踪可乐温度、剩余冰量、已融化冰水量和可乐浓度。为了让页面可以实时计算，模型做了以下简化：可乐近似为水溶液；杯中液体温度均匀；冰块用一个等效温度表示；杯壁和空气对可乐的加热合并为一个环境传热项；冰块形状不逐块建模，而用冰量近似表示总接触面积。</p>
          <p class="symbols">符号说明：m 表示质量，单位 g；T 表示温度，单位 °C；Q 表示热量，单位 J；c 表示比热容，单位 J/(g·°C)；Δt 表示数值模拟的时间步长。</p>
        </div>

        <div class="model-block">
          <h3>2. 传热原理：牛顿冷却定律的等效形式</h3>
          <p>传热的物理基础是牛顿冷却定律：单位时间传递的热量近似正比于温差。更标准的形式是 hA(T_hot - T_cold)Δt，其中 h 是换热系数，A 是接触面积。页面模型把难以直接测量的 h 和 A 合并成等效参数。</p>
          <div class="formula">
            <math display="block">
              <mrow>
                <mi>Q</mi><mo>=</mo><mi>h</mi><mi>A</mi><mo>(</mo><msub><mi>T</mi><mtext>hot</mtext></msub><mo>-</mo><msub><mi>T</mi><mtext>cold</mtext></msub><mo>)</mo><mi>Δt</mi>
              </mrow>
            </math>
          </div>
          <p class="symbols">符号说明：h 是换热系数，描述材料、流动和接触状态；A 是换热面积；T_hot 和 T_cold 分别是热端和冷端温度。这个公式是后面两个传热项的共同来源。</p>
        </div>

        <div class="model-block">
          <h3>3. 环境给可乐的热量</h3>
          <p>环境项表示空气和杯壁把热量传回可乐。这里没有显式写入可乐质量，不是说质量不重要，而是因为环境换热主要由杯子外表面积、杯壁材料和空气流动决定；这些因素在当前页面中被视为固定，并合并到 k_env 中。</p>
          <div class="formula">
            <math display="block">
              <mrow>
                <msub><mi>Q</mi><mtext>env</mtext></msub>
                <mo>=</mo>
                <msub><mi>k</mi><mtext>env</mtext></msub>
                <mo>(</mo><msub><mi>T</mi><mtext>air</mtext></msub><mo>-</mo><msub><mi>T</mi><mtext>cola</mtext></msub><mo>)</mo>
                <mi>Δt</mi>
              </mrow>
            </math>
          </div>
          <p class="symbols">符号说明：Q_env 是环境传给可乐的热量；k_env 是环境等效传热系数，已经包含杯壁面积和空气换热能力；T_air 是室温；T_cola 是可乐温度。当可乐低于室温时，这一项为正，可乐会回温。</p>
        </div>

        <div class="model-block">
          <h3>4. 可乐传给冰的热量</h3>
          <p>冰块项同样来自牛顿冷却定律。严格写法应该包含冰和可乐的接触面积 A_ice。为了实时交互，模型用剩余冰量 m_ice 近似接触面积：冰越多，通常总表面积越大，传热越快。这是经验闭合，不是基本物理定律。</p>
          <div class="formula">
            <math display="block">
              <mrow>
                <msub><mi>Q</mi><mtext>ice</mtext></msub>
                <mo>=</mo>
                <msub><mi>h</mi><mtext>ice</mtext></msub><msub><mi>A</mi><mtext>ice</mtext></msub>
                <mo>(</mo><msub><mi>T</mi><mtext>cola</mtext></msub><mo>-</mo><msub><mi>T</mi><mtext>ice</mtext></msub><mo>)</mo>
                <mi>Δt</mi>
              </mrow>
            </math>
            <math display="block">
              <mrow>
                <msub><mi>A</mi><mtext>ice</mtext></msub><mo>≈</mo><mi>α</mi><msub><mi>m</mi><mtext>ice</mtext></msub>
                <mo>⇒</mo>
                <msub><mi>Q</mi><mtext>ice</mtext></msub>
                <mo>=</mo>
                <msub><mi>k</mi><mtext>ice</mtext></msub><msub><mi>m</mi><mtext>ice</mtext></msub>
                <mo>(</mo><msub><mi>T</mi><mtext>cola</mtext></msub><mo>-</mo><msub><mi>T</mi><mtext>ice</mtext></msub><mo>)</mo>
                <mi>Δt</mi>
              </mrow>
            </math>
          </div>
          <p class="symbols">符号说明：Q_ice 是可乐传给冰的热量；h_ice 是冰和液体之间的换热系数；A_ice 是冰块总接触面积；α 是把冰量换算为等效接触面积的比例常数；k_ice = h_ice α。第二个公式有 m_ice，是为了近似“冰越多，接触面积越大”。</p>
        </div>

        <div class="model-block">
          <h3>5. 冰的升温与融化</h3>
          <p>冰拿到热量后并不会立刻全部变成水。若冰温低于 0°C，热量先用于把冰升温到 0°C；达到 0°C 后，后续热量主要用于相变融化。模型还把融化后的水升温到杯中液体温度所需的热量计入每克融冰的热量成本。</p>
          <div class="formula">
            <math display="block">
              <mrow>
                <msub><mi>Q</mi><mtext>warm</mtext></msub>
                <mo>=</mo>
                <msub><mi>m</mi><mtext>ice</mtext></msub><msub><mi>c</mi><mtext>ice</mtext></msub><mo>(</mo><mn>0</mn><mo>-</mo><msub><mi>T</mi><mtext>ice</mtext></msub><mo>)</mo>
              </mrow>
            </math>
            <math display="block">
              <mrow>
                <mi>dm</mi><mo>=</mo>
                <mfrac>
                  <msub><mi>Q</mi><mtext>left</mtext></msub>
                  <mrow><msub><mi>L</mi><mtext>f</mtext></msub><mo>+</mo><msub><mi>c</mi><mtext>water</mtext></msub><msub><mi>T</mi><mtext>cola</mtext></msub></mrow>
                </mfrac>
              </mrow>
            </math>
          </div>
          <p class="symbols">符号说明：Q_warm 是把冰从当前温度升到 0°C 需要的热量；c_ice 是冰的比热容；Q_left 是冰升温后剩余、可用于融化的热量；L_f 是冰的熔化潜热；c_water 是水的比热容；dm 是本时间步融化的冰质量。</p>
        </div>

        <div class="model-block">
          <h3>6. 可乐温度的数值更新</h3>
          <p>可乐的净热量等于环境输入减去冰吸走的热量。模型使用显式欧拉法逐步更新：每隔 Δt 秒计算一次热量交换，再更新温度、剩余冰量和融化水量。</p>
          <div class="formula">
            <math display="block">
              <mrow>
                <msub><mi>Q</mi><mtext>net</mtext></msub><mo>=</mo><msub><mi>Q</mi><mtext>env</mtext></msub><mo>-</mo><msub><mi>Q</mi><mtext>to ice</mtext></msub>
              </mrow>
            </math>
            <math display="block">
              <mrow>
                <msub><mi>T</mi><mtext>next</mtext></msub>
                <mo>=</mo>
                <msub><mi>T</mi><mtext>cola</mtext></msub>
                <mo>+</mo>
                <mfrac>
                  <msub><mi>Q</mi><mtext>net</mtext></msub>
                  <mrow><msub><mi>m</mi><mtext>liquid</mtext></msub><msub><mi>c</mi><mtext>cola</mtext></msub></mrow>
                </mfrac>
              </mrow>
            </math>
            <math display="block">
              <mrow>
                <msub><mi>m</mi><mtext>liquid</mtext></msub><mo>=</mo><msub><mi>m</mi><mtext>cola</mtext></msub><mo>+</mo><msub><mi>m</mi><mtext>melted</mtext></msub>
              </mrow>
            </math>
          </div>
          <p class="symbols">符号说明：Q_net 是可乐获得的净热量；Q_to ice 是真正被冰用于升温和融化的热量；T_next 是下一个时间步的可乐温度；m_liquid 是杯中液体质量。液体质量越大，同样热量造成的温度变化越小。</p>
        </div>

        <div class="model-block">
          <h3>7. 可乐浓度指标</h3>
          <p>页面中的浓度不是化学意义上的糖酸浓度，而是“原始可乐在液体总量中的质量占比”。它用于衡量融冰水造成的稀释。这个指标越接近 100%，表示饮料越接近原始可乐。</p>
          <div class="formula">
            <math display="block">
              <mrow>
                <mtext>concentration</mtext>
                <mo>=</mo>
                <mfrac>
                  <msub><mi>m</mi><mtext>cola</mtext></msub>
                  <mrow><msub><mi>m</mi><mtext>cola</mtext></msub><mo>+</mo><msub><mi>m</mi><mtext>melted</mtext></msub></mrow>
                </mfrac>
                <mo>×</mo><mn>100</mn><mo>%</mo>
              </mrow>
            </math>
          </div>
          <p class="symbols">符号说明：concentration 是页面显示的可乐浓度；m_cola 是初始可乐质量；m_melted 是已经融化进入液体的冰水质量。</p>
        </div>

        <div class="model-block">
          <h3>8. 评价指标：口感分数</h3>
          <p>口感分数不是物理定律，而是为了比较不同冰量而构造的经验评分。温度项采用“最佳区间”而不是“越冷越好”：Coca-Cola 的 fountain 成品饮料质量标准要求 finished drink temperature 保持在 32-40°F，约 0-4.4°C；碳酸饮料感官研究也显示，3°C 样品的 cooling、bite、burn、numbing 等碳酸刺激描述更强。因此模型把 0-4.4°C 视为最佳冷饮区间，超过 4.4°C 后逐渐扣分，低于冰点附近则不再继续加分。</p>
          <div class="formula">
            <math display="block">
              <mrow>
                <msub><mi>P</mi><mtext>temp</mtext></msub>
                <mo>=</mo>
                <mn>3.5</mn>
                <msup>
                  <mrow><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><msub><mi>T</mi><mtext>cola</mtext></msub><mo>-</mo><mn>4.4</mn><mo>)</mo></mrow>
                  <mn>1.35</mn>
                </msup>
              </mrow>
            </math>
            <math display="block">
              <mrow>
                <mtext>score</mtext>
                <mo>=</mo>
                <mn>70</mn>
                <mo>-</mo>
                <msub><mi>P</mi><mtext>temp</mtext></msub>
                <mo>+</mo>
                <mn>30</mn><mo>·</mo><mfrac><mtext>concentration</mtext><mn>100</mn></mfrac>
                <mo>-</mo>
                <mtext>占杯惩罚</mtext>
                <mo>-</mo>
                <mtext>融尽偏暖惩罚</mtext>
              </mrow>
            </math>
          </div>
          <p class="symbols">符号说明：P_temp 是温度偏离最佳冷饮区间的惩罚；4.4°C 来自 40°F 的换算；concentration 是上文定义的可乐浓度，越高越好。评分中 70 分给温度基础项，30 分给浓度项；冰量超过杯中可接受空间后扣“占杯惩罚”，冰融尽且仍高于 6°C 时扣“融尽偏暖惩罚”。这些权重是为了可视化比较而设定的经验权重，可用真实品评数据校准。</p>
          <p class="symbols">资料依据：Coca-Cola North America Quality Beverage Standards 要求成品 fountain drink 温度保持在 32-40°F；关于碳酸水的感官描述研究和综述显示，较低温度，尤其约 3°C，会增强 cooling、bite、burn、numbing 等与碳酸刺激相关的感知。</p>
        </div>

        <div class="model-block">
          <h3>9. 模型边界</h3>
          <p>这个模型适合解释趋势，但不是完整流体热传导仿真。它没有显式计算冰块真实几何形状、搅拌产生的对流、杯壁热容量、二氧化碳逸出和人的主观口味差异。最严谨的使用方式是把它作为实验设计和数据解释的基线，再用实测温度曲线校准 k_env 与 k_ice。</p>
        </div>
      </div>
    </section>
  </main>

  <script>
    const fixed = {
      colaMass: 300,
      colaTemp: 25,
      iceTemp: -18,
      ambientTemp: 25,
      drinkTime: 5,
      iceTransfer: 0.075,
      envTransfer: 0.25,
      colaCp: 4.0,
      waterCp: 4.18,
      iceCp: 2.1,
      fusion: 334.0,
      dt: 0.5,
      totalSeconds: 15 * 60
    };

    const iceSlider = document.getElementById("iceMass");
    const el = {
      iceMassVal: document.getElementById("iceMassVal"),
      tempMetric: document.getElementById("tempMetric"),
      tempNote: document.getElementById("tempNote"),
      dilutionMetric: document.getElementById("dilutionMetric"),
      cupCanvas: document.getElementById("cupCanvas"),
      iceVolumeBar: document.getElementById("iceVolumeBar"),
      cupCaption: document.getElementById("cupCaption")
    };

    function simulate(iceMass) {
      const n = Math.floor(fixed.totalSeconds / fixed.dt) + 1;
      const rows = [];
      let T = fixed.colaTemp;
      let ice = iceMass;
      let melted = 0;
      let liquid = fixed.colaMass;
      let iceTemp = fixed.iceTemp;

      for (let i = 0; i < n; i++) {
        const timeS = i * fixed.dt;
        rows.push({
          timeMin: timeS / 60,
          temperature: T,
          ice,
          melted,
          dilution: melted / fixed.colaMass * 100,
          concentration: fixed.colaMass / (fixed.colaMass + melted) * 100
        });

        const qEnv = fixed.envTransfer * (fixed.ambientTemp - T) * fixed.dt;
        let qToIce = 0;
        let dm = 0;

        if (ice > 1e-9 && T > 0) {
          const surfaceT = Math.max(iceTemp, 0);
          const heatTransfer = fixed.iceTransfer * ice * Math.max(T - surfaceT, 0);
          let qAvailable = heatTransfer * fixed.dt;

          if (iceTemp < 0) {
            const qWarmNeed = ice * fixed.iceCp * (0 - iceTemp);
            const qWarm = Math.min(qAvailable, qWarmNeed);
            iceTemp += qWarm / (ice * fixed.iceCp);
            qToIce += qWarm;
            qAvailable -= qWarm;
          }

          if (qAvailable > 0 && iceTemp >= -1e-9) {
            const heatPerMelt = fixed.fusion + fixed.waterCp * Math.max(T, 0);
            dm = Math.min(ice, qAvailable / heatPerMelt);
            qToIce += dm * heatPerMelt;
          }
        }

        const heatCapacity = liquid * fixed.colaCp;
        T = Math.max(T + (qEnv - qToIce) / heatCapacity, ice - dm > 1e-9 ? 0 : -5);
        ice = Math.max(0, ice - dm);
        melted += dm;
        liquid += dm;
        if (ice <= 1e-9) iceTemp = 0;
      }
      return rows;
    }

    function atMinute(rows, minute) {
      let best = rows[0], bestDelta = Math.abs(rows[0].timeMin - minute);
      for (const row of rows) {
        const delta = Math.abs(row.timeMin - minute);
        if (delta < bestDelta) {
          best = row;
          bestDelta = delta;
        }
      }
      return best;
    }

    function temperatureSuitability(T) {
      if (T <= 4.4) return 100;
      if (T <= 15) return 100 * (15 - T) / (15 - 4.4);
      return 0;
    }

    function tasteScore(row, initialIce) {
      const tempScore = 65 * temperatureSuitability(row.temperature) / 100;
      const concentrationScore = 35 * row.concentration / 100;
      const crowdingPenalty = 0.22 * Math.max(0, initialIce - 0.6 * fixed.colaMass);
      const noIcePenalty = row.ice <= 0 && row.temperature > 6 ? 8 : 0;
      return Math.max(0, Math.min(100, tempScore + concentrationScore - crowdingPenalty - noIcePenalty));
    }

    function scanIce() {
      const rows = [];
      for (let ice = 0; ice <= 300; ice += 5) {
        const sim = simulate(ice);
        const row = atMinute(sim, fixed.drinkTime);
        rows.push({
          ice,
          temperature: row.temperature,
          dilution: row.dilution,
          temperatureSuitability: temperatureSuitability(row.temperature),
          concentration: row.concentration,
          melted: row.melted,
          score: tasteScore(row, ice)
        });
      }
      return rows;
    }

    function drawCurve(canvas, current, recommended) {
      const ctx = canvas.getContext("2d");
      const w = canvas.width, h = canvas.height;
      const pad = {left: 54, right: 58, top: 24, bottom: 44};
      const plotW = w - pad.left - pad.right;
      const plotH = h - pad.top - pad.bottom;
      const x = v => pad.left + v / 15 * plotW;
      const y = v => pad.top + (1 - v / 30) * plotH;
      const yPct = v => pad.top + (1 - v / 100) * plotH;

      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = "#fffdfa";
      ctx.fillRect(0, 0, w, h);
      ctx.fillStyle = "rgba(72, 122, 85, 0.13)";
      ctx.fillRect(pad.left, y(6), plotW, y(0) - y(6));

      drawGrid(ctx, pad, plotW, plotH, w, h, 15, 30, "时间 (min)", "温度 (°C)");
      drawRightAxis(ctx, pad, plotW, plotH, w, "可乐浓度 (%)");
      drawLine(ctx, current.map(r => [r.timeMin, r.temperature]), x, y, "#1572a6", 3);
      drawLine(ctx, current.map(r => [r.timeMin, r.concentration]), x, yPct, "#c7473f", 2.4);
    }

    function drawRightAxis(ctx, pad, plotW, plotH, w, label) {
      const axisX = pad.left + plotW;
      const y = v => pad.top + (1 - v / 100) * plotH;

      ctx.save();
      ctx.strokeStyle = "#666059";
      ctx.fillStyle = "#666059";
      ctx.lineWidth = 1;
      ctx.font = "13px system-ui, sans-serif";

      ctx.beginPath();
      ctx.moveTo(axisX, pad.top);
      ctx.lineTo(axisX, pad.top + plotH);
      ctx.stroke();

      for (let pct = 0; pct <= 100; pct += 20) {
        const yy = y(pct);
        ctx.beginPath();
        ctx.moveTo(axisX, yy);
        ctx.lineTo(axisX + 5, yy);
        ctx.stroke();
        ctx.fillText(pct.toString(), axisX + 9, yy + 4);
      }

      ctx.translate(w - 12, pad.top + plotH / 2 + 42);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText(label, 0, 0);
      ctx.restore();
    }

    function drawScan(canvas, scan, currentIce, bestIce) {
      const ctx = canvas.getContext("2d");
      const w = canvas.width, h = canvas.height;
      const pad = {left: 52, right: 54, top: 24, bottom: 44};
      const plotW = w - pad.left - pad.right;
      const plotH = h - pad.top - pad.bottom;
      const x = v => pad.left + v / 300 * plotW;
      const yTemp = v => pad.top + (1 - v / 30) * plotH;
      const yPct = v => pad.top + (1 - v / 100) * plotH;

      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = "#fffdfa";
      ctx.fillRect(0, 0, w, h);
      drawGrid(ctx, pad, plotW, plotH, w, h, 300, 30, "冰量 (g)", "温度 (°C)");
      drawRightAxis(ctx, pad, plotW, plotH, w, "浓度 (%)");

      drawLine(ctx, scan.map(r => [r.ice, r.temperature]), x, yTemp, "#1572a6", 3);
      drawLine(ctx, scan.map(r => [r.ice, r.concentration]), x, yPct, "#c7473f", 2.4);

      for (const marker of [{ice: currentIce, color: "#181817"}, {ice: bestIce, color: "#c7473f"}]) {
        ctx.beginPath();
        ctx.strokeStyle = marker.color;
        ctx.setLineDash([5, 5]);
        ctx.moveTo(x(marker.ice), pad.top);
        ctx.lineTo(x(marker.ice), pad.top + plotH);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      ctx.fillStyle = "#666059";
      ctx.font = "13px system-ui, sans-serif";
      ctx.fillText("浓度", w - 42, 18);
    }

    function drawGrid(ctx, pad, plotW, plotH, w, h, xMax, yMax, xLabel, yLabel) {
      const x = v => pad.left + v / xMax * plotW;
      const y = v => pad.top + (1 - v / yMax) * plotH;
      ctx.strokeStyle = "#ded6ca";
      ctx.lineWidth = 1;
      ctx.font = "13px system-ui, sans-serif";
      ctx.fillStyle = "#666059";

      for (let i = 0; i <= 5; i++) {
        const xv = xMax * i / 5;
        ctx.beginPath();
        ctx.moveTo(x(xv), pad.top);
        ctx.lineTo(x(xv), pad.top + plotH);
        ctx.stroke();
        ctx.fillText(Math.round(xv).toString(), x(xv) - 8, h - 18);
      }

      for (let i = 0; i <= 5; i++) {
        const yv = yMax * i / 5;
        ctx.beginPath();
        ctx.moveTo(pad.left, y(yv));
        ctx.lineTo(pad.left + plotW, y(yv));
        ctx.stroke();
        ctx.fillText(Math.round(yv).toString(), 16, y(yv) + 4);
      }

      ctx.strokeStyle = "#666059";
      ctx.strokeRect(pad.left, pad.top, plotW, plotH);
      ctx.fillText(xLabel, pad.left + plotW / 2 - 30, h - 6);
      ctx.save();
      ctx.translate(14, pad.top + plotH / 2 + 36);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText(yLabel, 0, 0);
      ctx.restore();
    }

    function drawLine(ctx, points, x, y, color, width, dash = []) {
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.lineWidth = width;
      ctx.setLineDash(dash);
      points.forEach(([px, py], idx) => {
        if (idx === 0) ctx.moveTo(x(px), y(py));
        else ctx.lineTo(x(px), y(py));
      });
      ctx.stroke();
      ctx.setLineDash([]);
    }

    function cupHalfWidthAt(y, geom) {
      const t = Math.max(0, Math.min(1, (y - geom.top) / geom.height));
      return geom.topHalf + (geom.bottomHalf - geom.topHalf) * t;
    }

    function cupVolumeBelow(levelY, geom) {
      const slices = 160;
      const start = Math.max(geom.top, Math.min(geom.bottom, levelY));
      const end = geom.bottom;
      let area = 0;
      for (let i = 0; i < slices; i++) {
        const y = start + (end - start) * (i + 0.5) / slices;
        area += cupHalfWidthAt(y, geom) * 2 * Math.abs(end - start) / slices;
      }
      return area;
    }

    function levelForVolume(volumeMl, geom, pxPerMl) {
      const targetArea = volumeMl * pxPerMl;
      let lo = geom.top;
      let hi = geom.bottom;
      for (let i = 0; i < 34; i++) {
        const mid = (lo + hi) / 2;
        if (cupVolumeBelow(mid, geom) > targetArea) lo = mid;
        else hi = mid;
      }
      return (lo + hi) / 2;
    }

    function cupPath(ctx, geom) {
      ctx.beginPath();
      ctx.moveTo(geom.cx - geom.topHalf, geom.top);
      ctx.lineTo(geom.cx + geom.topHalf, geom.top);
      ctx.quadraticCurveTo(geom.cx + geom.bottomHalf + 10, geom.top - 150, geom.cx + geom.bottomHalf, geom.bottom);
      ctx.quadraticCurveTo(geom.cx, geom.bottom - 24, geom.cx - geom.bottomHalf, geom.bottom);
      ctx.quadraticCurveTo(geom.cx - geom.bottomHalf - 10, geom.top - 150, geom.cx - geom.topHalf, geom.top);
      ctx.closePath();
    }

    function drawIceCube(ctx, x, y, size, rot, waterY, submergedRatio) {
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(rot * Math.PI / 180);
      const w = size;
      const h = size * 0.78;
      ctx.beginPath();
      roundRectPath(ctx, -w / 2, -h / 2, w, h, 7);
      ctx.fillStyle = "rgba(222, 246, 255, .92)";
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = "rgba(91, 164, 204, .76)";
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(-w * .25, -h * .25);
      ctx.lineTo(w * .18, -h * .10);
      ctx.lineTo(w * .08, h * .22);
      ctx.strokeStyle = "rgba(255,255,255,.74)";
      ctx.stroke();
      ctx.restore();

      ctx.save();
      ctx.beginPath();
      ctx.rect(x - size, waterY, size * 2, size);
      ctx.clip();
      ctx.globalAlpha = 0.24 + 0.18 * submergedRatio;
      ctx.fillStyle = "#6eb6d8";
      ctx.beginPath();
      ctx.arc(x, y + size * .1, size * .46, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    function roundRectPath(ctx, x, y, w, h, r) {
      ctx.moveTo(x + r, y);
      ctx.lineTo(x + w - r, y);
      ctx.quadraticCurveTo(x + w, y, x + w, y + r);
      ctx.lineTo(x + w, y + h - r);
      ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
      ctx.lineTo(x + r, y + h);
      ctx.quadraticCurveTo(x, y + h, x, y + h - r);
      ctx.lineTo(x, y + r);
      ctx.quadraticCurveTo(x, y, x + r, y);
    }

    function renderCup(iceMass, row) {
      const canvas = el.cupCanvas;
      const ctx = canvas.getContext("2d");
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);

      const geom = {
        cx: w / 2,
        top: 44,
        bottom: 378,
        topHalf: 110,
        bottomHalf: 70,
        height: 334
      };
      const cupCapacityMl = 560;
      const fullArea = cupVolumeBelow(geom.top, geom);
      const pxPerMl = fullArea / cupCapacityMl;
      const colaVolumeMl = fixed.colaMass;
      const iceVolumeMl = iceMass / 0.917;
      const displacedMl = iceMass; // floating ice displaces its own mass of liquid.
      const waterLevelY = levelForVolume(colaVolumeMl + displacedMl, geom, pxPerMl);
      const noIceLevelY = levelForVolume(colaVolumeMl, geom, pxPerMl);
      const fillRisk = colaVolumeMl + displacedMl > cupCapacityMl;

      ctx.save();
      cupPath(ctx, geom);
      ctx.clip();

      const liquid = ctx.createLinearGradient(0, waterLevelY, 0, geom.bottom);
      liquid.addColorStop(0, "#82391f");
      liquid.addColorStop(.55, "#4c1d12");
      liquid.addColorStop(1, "#2c100b");
      ctx.fillStyle = liquid;
      ctx.fillRect(geom.cx - geom.topHalf - 12, waterLevelY, geom.topHalf * 2 + 24, geom.bottom - waterLevelY + 12);

      ctx.fillStyle = "rgba(255, 238, 200, .72)";
      ctx.fillRect(geom.cx - cupHalfWidthAt(waterLevelY, geom) + 7, waterLevelY - 2, cupHalfWidthAt(waterLevelY, geom) * 2 - 14, 4);

      const cubeCount = Math.min(18, Math.round(iceMass / 18));
      const positions = [
        [-48, -18, -10], [2, -12, 12], [48, -16, 8], [-22, 18, -18], [32, 20, 17],
        [-60, 32, -7], [66, 36, 21], [0, 48, -15], [-34, 58, 9], [38, 66, -8],
        [-8, -46, 14], [58, -48, -22], [-58, -50, 6], [18, 86, 4], [-54, 92, -12],
        [60, 100, 15], [-6, 112, -5], [36, 126, 11]
      ];
      const cubeSize = 34;
      const submergedRatio = 0.917;
      const exposedPx = cubeSize * (1 - submergedRatio);
      for (let i = 0; i < cubeCount; i++) {
        const [dx, dy, rot] = positions[i];
        const x = geom.cx + dx;
        const y = Math.min(geom.bottom - 26, waterLevelY - exposedPx + dy);
        const half = cupHalfWidthAt(y, geom) - 18;
        const clampedX = Math.max(geom.cx - half, Math.min(geom.cx + half, x));
        drawIceCube(ctx, clampedX, y, cubeSize, rot, waterLevelY, submergedRatio);
      }

      ctx.restore();

      ctx.save();
      cupPath(ctx, geom);
      ctx.lineWidth = 6;
      ctx.strokeStyle = "rgba(92, 83, 72, .58)";
      ctx.stroke();
      ctx.lineWidth = 2;
      ctx.strokeStyle = "rgba(255,255,255,.72)";
      ctx.stroke();
      ctx.restore();

      ctx.fillStyle = "rgba(255,255,255,.45)";
      ctx.beginPath();
      roundRectPath(ctx, geom.cx - 82, geom.top + 18, 22, 232, 12);
      ctx.fill();

      ctx.strokeStyle = "#ad7419";
      ctx.setLineDash([4, 5]);
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(geom.cx + geom.topHalf + 16, noIceLevelY);
      ctx.lineTo(geom.cx + geom.topHalf + 58, noIceLevelY);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#766b5f";
      ctx.font = "14px system-ui, sans-serif";
      ctx.fillText("原液面", geom.cx + geom.topHalf + 12, noIceLevelY - 8);

      if (fillRisk) {
        ctx.fillStyle = "#c7473f";
        ctx.font = "13px system-ui, sans-serif";
        ctx.fillText("可能溢出", geom.cx - 32, geom.top - 14);
      }

      const iceShare = iceVolumeMl / (colaVolumeMl + iceVolumeMl || 1) * 100;
      const liquidRiseMl = displacedMl;
      el.iceVolumeBar.style.width = `${Math.min(100, iceShare)}%`;
      el.cupCaption.textContent = `冰体积约占 ${iceShare.toFixed(0)}%；浮冰让液面相当于多了约 ${liquidRiseMl.toFixed(0)} mL 排水量。`;
    }

    function update() {
      const iceMass = +iceSlider.value;
      const sim = simulate(iceMass);
      const row = atMinute(sim, fixed.drinkTime);
      const scan = scanIce();
      const best = scan.reduce((a, b) => b.score > a.score ? b : a, scan[0]);
      const bestSim = simulate(best.ice);

      el.iceMassVal.textContent = `${iceMass} g`;
      el.tempMetric.textContent = `${row.temperature.toFixed(1)}°C`;
      el.tempNote.textContent = row.temperature <= 6 ? "已经进入冰爽区。" : "还不够冰爽。";
      el.dilutionMetric.textContent = `${row.concentration.toFixed(1)}%`;
      renderCup(iceMass, row);

      drawCurve(document.getElementById("curveCanvas"), sim, bestSim);
      drawScan(document.getElementById("scanCanvas"), scan, iceMass, best.ice);
    }

    iceSlider.addEventListener("input", update);
    update();
  </script>
</body>
</html>
"""


def main() -> None:
    Path("cola_ice_visual_model.html").write_text(HTML, encoding="utf-8")
    print("Generated simplified cola_ice_visual_model.html")


if __name__ == "__main__":
    main()
