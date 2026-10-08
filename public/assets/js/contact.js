/* ==========================================================================
   RivesEnRêves — formulaire de contact segmenté par univers
   --------------------------------------------------------------------------
   CONFIGURATION (à renseigner une seule fois)
   --------------------------------------------------------------------------
   Les valeurs ci-dessous sont remplies automatiquement par build.py à partir
   de config.json. Si vous modifiez directement les fichiers en ligne (sans
   build.py), remplacez simplement les marqueurs entre crochets ici.

   - EMAIL_RECEPTION : adresse qui reçoit les messages
     → contact@rivesenreves.com
   - WEB3FORMS_KEY   : laisser vide pour utiliser FormSubmit (gratuit, sans
     compte) ; renseigner pour utiliser Web3Forms (gratuit, avec clé).
   ========================================================================== */
var CONTACT_CONFIG = {
  EMAIL_RECEPTION: "contact@rivesenreves.com",
  WEB3FORMS_KEY: "[WEB3FORMS_ACCESS_KEY]"
};

(function () {
  "use strict";

  var form = document.getElementById("contact-form");
  if (!form) return;

  var cfg = CONTACT_CONFIG;
  var useWeb3 = cfg.WEB3FORMS_KEY && cfg.WEB3FORMS_KEY.charAt(0) !== "[";
  var emailOk = cfg.EMAIL_RECEPTION && cfg.EMAIL_RECEPTION.charAt(0) !== "[";

  // Libellés utilisés dans l'objet de l'e-mail reçu : « [Plaisancier] Nouvelle demande de contact »
  var LABELS = {
    particulier: "Balade",
    plaisancier: "Plaisancier",
    professionnel: "Professionnel",
    administration: "Administration"
  };

  var status = document.getElementById("form-status");
  var subject = form.querySelector('input[name="_subject"]');
  var radios = form.querySelectorAll('input[name="profil"]');
  var groups = form.querySelectorAll("[data-profil-fields]");
  var submit = form.querySelector('button[type="submit"]');
  var next = form.querySelector('input[name="_next"]');

  // Adresse de repli sans JavaScript (FormSubmit classique + page merci)
  if (emailOk) form.action = "https://formsubmit.co/" + encodeURIComponent(cfg.EMAIL_RECEPTION);
  if (next) next.value = new URL("merci/", window.location.href.split("?")[0].split("#")[0]).href;

  /* Champs complémentaires affichés selon le profil ---------------------- */
  function currentProfil() {
    var r = form.querySelector('input[name="profil"]:checked');
    return r ? r.value : "";
  }

  function updateProfil() {
    var p = currentProfil();
    groups.forEach(function (g) {
      var show = g.getAttribute("data-profil-fields") === p;
      g.hidden = !show;
      // Les champs masqués ne sont ni envoyés ni bloquants
      g.querySelectorAll("input, select, textarea").forEach(function (f) { f.disabled = !show; });
    });
    if (subject) {
      subject.value = (p ? "[" + LABELS[p] + "] " : "") + "Nouvelle demande de contact";
    }
    // Accent de couleur du formulaire selon l'univers choisi
    var map = { particulier: "u-balades", plaisancier: "u-plaisanciers", professionnel: "u-professionnels", administration: "u-administrations" };
    form.classList.remove("u-balades", "u-plaisanciers", "u-professionnels", "u-administrations");
    if (map[p]) form.classList.add(map[p]);
  }

  radios.forEach(function (r) { r.addEventListener("change", updateProfil); });

  /* Présélection depuis l'URL : contact/?profil=plaisancier&objet=etude-vnf */
  var params = new URLSearchParams(window.location.search);
  var preset = params.get("profil");
  if (preset) {
    var r = form.querySelector('input[name="profil"][value="' + preset.replace(/[^a-z]/g, "") + '"]');
    if (r) r.checked = true;
  }
  var objet = params.get("objet");
  var objetField = form.querySelector('[data-profil-fields="' + currentProfil() + '"] [name="demande"]');
  if (objet && objetField) {
    var opt = objetField.querySelector('option[value="' + objet.replace(/[^a-z0-9-]/g, "") + '"]');
    if (opt) objetField.value = opt.value;
  }
  updateProfil();

  /* Envoi ---------------------------------------------------------------- */
  function show(type, msg) {
    status.hidden = false;
    status.className = "form-status is-" + type;
    status.textContent = msg;
    status.focus();
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (!form.checkValidity()) {
      form.querySelectorAll(":invalid").forEach(function (f) { f.setAttribute("aria-invalid", "true"); });
      var first = form.querySelector(":invalid");
      if (first) first.focus();
      show("error", "Merci de compléter les champs obligatoires signalés.");
      return;
    }
    form.querySelectorAll("[aria-invalid]").forEach(function (f) { f.removeAttribute("aria-invalid"); });

    // Piège à robots : un humain ne remplit jamais ce champ invisible
    var hp = form.querySelector('input[name="_honey"]');
    if (hp && hp.value) { show("success", "Merci, votre message a bien été envoyé."); form.reset(); return; }

    if (!useWeb3 && !emailOk) {
      show("error", "Le formulaire n'est pas encore configuré (adresse de réception manquante). Écrivez-nous directement par e-mail.");
      return;
    }

    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    // Objet de la demande : libellé lisible plutôt que le code technique
    var demande = form.querySelector('select[name="demande"]:not(:disabled)');
    if (demande) { data["Demande"] = demande.options[demande.selectedIndex].text; }
    delete data.demande;
    var p = data.profil;
    data["Profil"] = LABELS[p] || p;
    delete data.profil;
    data["Page d'origine"] = document.referrer || window.location.href;

    var url, payload;
    if (useWeb3) {
      url = "https://api.web3forms.com/submit";
      payload = data;
      payload.access_key = cfg.WEB3FORMS_KEY;
      payload.subject = data._subject;
      payload.from_name = "Site RivesEnRêves";
      payload.botcheck = "";
      delete payload._subject; delete payload._honey; delete payload._next; delete payload._template; delete payload._captcha;
    } else {
      url = "https://formsubmit.co/ajax/" + encodeURIComponent(cfg.EMAIL_RECEPTION);
      payload = data;
      delete payload._next;
    }

    submit.disabled = true;
    var label = submit.textContent;
    submit.textContent = "Envoi en cours…";

    fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (res) { return res.json().then(function (j) { return { ok: res.ok, body: j }; }); })
      .then(function (r) {
        var success = r.ok && (r.body.success === true || r.body.success === "true");
        if (!success) throw new Error(r.body && r.body.message ? r.body.message : "Erreur d'envoi");
        form.reset();
        updateProfil();
        show("success", "Merci ! Votre message a bien été envoyé. Nous vous répondons dans les meilleurs délais.");
      })
      .catch(function () {
        show("error", "Votre message n'a pas pu être envoyé (connexion ou service indisponible). Réessayez dans un instant ou écrivez-nous directement à l'adresse indiquée à droite.");
      })
      .then(function () {
        submit.disabled = false;
        submit.textContent = label;
      });
  });
})();
