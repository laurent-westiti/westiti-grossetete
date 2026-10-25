/*
  Page « Créer ma grosse tête » : l'aperçu en direct.

  La photo ne quitte pas le navigateur tant que la commande n'est pas
  envoyée. L'aperçu la place dans la forme du panneau, avec la marge blanche
  qu'aura la découpe, et suit chaque choix : recadrage, taille, quantité.

  Le détourage au contour des cheveux viendra du serveur. En attendant, la
  forme montrée est un ovale, qui suffit à juger du cadrage.
*/
(function () {
  var C = window.GROSSE_TETE;
  var toile = document.getElementById('toile');
  var ctx = toile.getContext('2d');
  var W = toile.width, H = toile.height;

  // La forme du panneau dans la toile.
  var forme = { cx: W / 2, cy: 450, rx: 290, ry: 350, marge: 16 };

  var etat = { image: null, zoom: 1, x: 0, y: 0 };

  var champ = function (id) { return document.getElementById(id); };
  var entree = champ('photo'), depot = champ('depot');
  var zoom = champ('zoom'), bouton = champ('commander'), manque = champ('manque');
  var accord = champ('accord');

  // ------------------------------------------------------------ dessin

  function ovale(c, rx, ry) {
    c.beginPath();
    c.ellipse(forme.cx, forme.cy, rx, ry, 0, 0, Math.PI * 2);
  }

  function dessiner() {
    ctx.clearRect(0, 0, W, H);

    // Le manche, derrière le panneau.
    ctx.fillStyle = '#C9B79C';
    ctx.fillRect(forme.cx - 13, forme.cy + forme.ry - 40, 26, H);
    ctx.fillStyle = 'rgba(0,0,0,.08)';
    ctx.fillRect(forme.cx + 5, forme.cy + forme.ry - 40, 8, H);

    // La marge blanche de la découpe, et son ombre.
    ctx.save();
    ctx.shadowColor = 'rgba(12,26,24,.22)';
    ctx.shadowBlur = 34; ctx.shadowOffsetY = 14;
    ovale(ctx, forme.rx + forme.marge, forme.ry + forme.marge);
    ctx.fillStyle = '#fff'; ctx.fill();
    ctx.restore();

    if (!etat.image) {
      ovale(ctx, forme.rx, forme.ry);
      ctx.fillStyle = '#F1EBE1'; ctx.fill();
      ctx.setLineDash([14, 12]); ctx.lineWidth = 4; ctx.strokeStyle = '#D8CDBB';
      ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = '#A9B5B1';
      ctx.font = '600 34px Gabarito, sans-serif'; ctx.textAlign = 'center';
      ctx.fillText('Sa photo ici', forme.cx, forme.cy + 12);
      return;
    }

    // La photo, cadrée dans l'ovale.
    var img = etat.image;
    var boiteL = forme.rx * 2, boiteH = forme.ry * 2;
    var base = Math.max(boiteL / img.width, boiteH / img.height);
    var echelle = base * etat.zoom;
    var l = img.width * echelle, h = img.height * echelle;
    borner(l, h);
    ctx.save();
    ovale(ctx, forme.rx, forme.ry);
    ctx.clip();
    ctx.drawImage(img, forme.cx - l / 2 + etat.x, forme.cy - h / 2 + etat.y, l, h);
    ctx.restore();

    champ('champ-zoom').value = etat.zoom.toFixed(3);
    champ('champ-x').value = (etat.x / boiteL).toFixed(4);
    champ('champ-y').value = (etat.y / boiteH).toFixed(4);
  }

  // La photo ne doit jamais laisser de vide dans l'ovale.
  function borner(l, h) {
    var mx = Math.max(0, (l - forme.rx * 2) / 2);
    var my = Math.max(0, (h - forme.ry * 2) / 2);
    etat.x = Math.max(-mx, Math.min(mx, etat.x));
    etat.y = Math.max(-my, Math.min(my, etat.y));
  }

  // ------------------------------------------------------------ la photo

  function charger(fichier) {
    if (!fichier) return;
    if (fichier.size > C.photoMaxMo * 1024 * 1024) {
      signaler('Cette photo dépasse ' + C.photoMaxMo + ' Mo. Choisis-en une plus légère.');
      return;
    }
    var url = URL.createObjectURL(fichier);
    var img = new Image();
    img.onload = function () {
      etat.image = img; etat.zoom = 1; etat.x = 0; etat.y = 0; zoom.value = 1;
      toile.classList.remove('vide');
      champ('legende').textContent = 'Fais glisser pour centrer le visage';
      champ('recadrer').classList.add('visible');
      depot.classList.add('rempli');
      champ('depot-titre').textContent = fichier.name;
      champ('depot-detail').textContent = 'Changer de photo';
      if (img.width < 800 || img.height < 800) {
        signaler('Cette photo est un peu petite : le visage risque d\'être flou une fois imprimé en grand. Une photo plus grande donnera un meilleur résultat.');
      } else {
        signaler('');
      }
      dessiner(); mettreAJour();
    };
    img.onerror = function () {
      signaler('Nous n\'arrivons pas à lire cette photo. Essaie avec un fichier JPEG ou PNG.');
    };
    img.src = url;
  }

  var avis = null;
  function signaler(texte) {
    if (!avis) {
      avis = document.createElement('p');
      avis.className = 'aide';
      avis.style.cssText = 'margin:12px 0 0; color:var(--corail-fonce);';
      depot.insertAdjacentElement('afterend', avis);
    }
    avis.textContent = texte;
    avis.hidden = !texte;
  }

  entree.addEventListener('change', function () { charger(entree.files[0]); });

  ['dragenter', 'dragover'].forEach(function (t) {
    depot.addEventListener(t, function (e) { e.preventDefault(); depot.classList.add('survol'); });
  });
  ['dragleave', 'drop'].forEach(function (t) {
    depot.addEventListener(t, function (e) { e.preventDefault(); depot.classList.remove('survol'); });
  });
  depot.addEventListener('drop', function (e) {
    if (!e.dataTransfer.files.length) return;
    entree.files = e.dataTransfer.files;
    charger(entree.files[0]);
  });

  // ------------------------------------------------------------ recadrage

  zoom.addEventListener('input', function () { etat.zoom = parseFloat(zoom.value); dessiner(); });

  var prise = null;
  toile.addEventListener('pointerdown', function (e) {
    if (!etat.image) return;
    prise = { x: e.clientX, y: e.clientY, ox: etat.x, oy: etat.y };
    toile.setPointerCapture(e.pointerId);
    toile.style.cursor = 'grabbing';
  });
  toile.addEventListener('pointermove', function (e) {
    if (!prise) return;
    var r = toile.getBoundingClientRect(), k = W / r.width;
    etat.x = prise.ox + (e.clientX - prise.x) * k;
    etat.y = prise.oy + (e.clientY - prise.y) * k;
    dessiner();
  });
  ['pointerup', 'pointercancel'].forEach(function (t) {
    toile.addEventListener(t, function () { prise = null; toile.style.cursor = ''; });
  });

  // ------------------------------------------------------- taille, prix

  function euros(n) {
    var arrondi = Math.round(n * 100) / 100;
    var texte = arrondi % 1 === 0 ? String(arrondi) : arrondi.toFixed(2).replace('.', ',');
    return texte + ' €';
  }

  function quantiteChoisie() {
    var r = document.querySelector('input[name=quantite]:checked');
    return r ? parseInt(r.value, 10) : 1;
  }

  function tailleChoisie() {
    var r = document.querySelector('input[name=taille]:checked');
    return r ? r.value : null;
  }

  function mettreAJour() {
    var t = tailleChoisie();
    var info = t ? C.tailles[t] : null;
    document.querySelectorAll('#echelles [data-taille]').forEach(function (d) {
      d.hidden = d.getAttribute('data-taille') !== t;
    });
    champ('r-taille').textContent = info ? info.hauteur + ' cm' : '—';
    var q = quantiteChoisie();
    champ('r-quantite').textContent = q;
    var total = info ? info.prix[q] : 0;

    // Les cartes de quantité affichent les prix de la taille choisie.
    if (info) {
      [1, 2, 3].forEach(function (n) {
        var t = document.querySelector('[data-q="' + n + '"]');
        var g = document.querySelector('[data-gain="' + n + '"]');
        if (t) t.textContent = euros(info.prix[n]);
        if (g && n > 1) {
          g.innerHTML = 'La ' + n + '<sup>e</sup> pour +' + euros(info.prix[n] - info.prix[n - 1])
            + ', soit ' + euros(info.prix[n] / n) + ' la tête';
        }
      });
    }
    champ('r-total').textContent = info ? euros(total) : '—';

    var prete = etat.image && info && accord.checked;
    bouton.disabled = !prete;
    bouton.textContent = prete ? 'Commander — ' + euros(total) : 'Commander';
    var mb = champ('m-commander');
    mb.disabled = !prete;
    champ('m-total').textContent = info ? euros(total) : '—';
    champ('m-manque').textContent = !etat.image ? 'Ajoute une photo'
      : !info ? 'Choisis une taille'
      : !accord.checked ? 'Confirme l\'accord'
      : q + ' × ' + info.hauteur + ' cm';
    manque.textContent = !etat.image ? 'Ajoute une photo pour continuer.'
      : !info ? 'Choisis une taille pour continuer.'
      : !accord.checked ? 'Confirme l\'accord de la personne pour continuer.'
      : 'Tout est prêt.';
  }

  document.querySelectorAll('input[name=taille]').forEach(function (r) {
    r.addEventListener('change', mettreAJour);
  });
  accord.addEventListener('change', mettreAJour);
  document.querySelectorAll('input[name=quantite]').forEach(function (r) {
    r.addEventListener('change', mettreAJour);
  });

  champ('formulaire').addEventListener('submit', function () {
    [bouton, champ('m-commander')].forEach(function (b) {
      b.disabled = true; b.textContent = 'Un instant…';
    });
  });

  // Les polices doivent être prêtes avant le premier dessin de la toile.
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
    dessiner(); mettreAJour();
  });
})();
